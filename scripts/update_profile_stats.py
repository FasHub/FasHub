#!/usr/bin/env python3
"""Refresh aggregate GitHub profile statistics; never fetch repository contents."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

METADATA = '''query($login: String!, $cursor: String) {
  user(login: $login) {
    login createdAt followers { totalCount }
    contributionsCollection { contributionYears }
    publicRepositories: repositories(privacy: PUBLIC, ownerAffiliations: [OWNER]) { totalCount }
    starRepositories: repositories(first: 100, after: $cursor, privacy: PUBLIC,
                                  ownerAffiliations: [OWNER], isFork: false) {
      nodes { stargazerCount }
      pageInfo { hasNextPage endCursor }
    }
  }
}'''
ANNUAL = '''query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}'''
START = '<!-- profile-stats:start -->'
END = '<!-- profile-stats:end -->'


def query_github(query, variables):
    payload = json.dumps({'query': query, 'variables': variables}).encode()
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        request = urllib.request.Request('https://api.github.com/graphql', data=payload,
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',
                     'User-Agent': 'FasHub-profile-stats'})
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
    else:
        # Local preview uses the existing CLI login. No credentials are saved.
        response = subprocess.run(['gh', 'api', 'graphql', '--input', '-'], input=payload,
                                  capture_output=True, check=True, timeout=60)
        result = json.loads(response.stdout)
    if result.get('errors') or not result.get('data', {}).get('user'):
        raise RuntimeError('GitHub did not return complete profile statistics.')
    return result['data']['user']


def year_windows(years, now):
    years = sorted({int(year) for year in years if int(year) <= now.year} | {now.year})
    return [(year, f'{year}-01-01T00:00:00Z',
             now.strftime('%Y-%m-%dT%H:%M:%SZ') if year == now.year
             else f'{year}-12-31T23:59:59Z') for year in years]


def summarize(rows, current_year):
    current = next(row for row in rows if row['year'] == current_year)
    return {'commits_year': current['commits'],
            'commits_all_time': sum(row['commits'] for row in rows),
            'contributions_year': current['contributions'],
            'contributions_all_time': sum(row['contributions'] for row in rows)}


def monthly_counts(days, now):
    counts = [0] * now.month
    for day in days:
        date = datetime.strptime(day['date'], '%Y-%m-%d').date()
        if date.year == now.year and date <= now.date():
            counts[date.month - 1] += day['contributionCount']
    return counts


def collect(login, now):
    metadata = query_github(METADATA, {'login': login, 'cursor': None})
    page = metadata['starRepositories']
    stars = sum(repo['stargazerCount'] for repo in page['nodes'])
    while page['pageInfo']['hasNextPage']:
        page = query_github(METADATA, {'login': login, 'cursor': page['pageInfo']['endCursor']})['starRepositories']
        stars += sum(repo['stargazerCount'] for repo in page['nodes'])
    rows, months = [], []
    for year, start, end in year_windows(metadata['contributionsCollection']['contributionYears'], now):
        result = query_github(ANNUAL, {'login': login, 'from': start, 'to': end})['contributionsCollection']
        cal = result['contributionCalendar']
        rows.append({'year': year, 'commits': result['totalCommitContributions'],
                     'contributions': cal['totalContributions'],
                     'restricted': result['restrictedContributionsCount']})
        if year == now.year:
            days = [day for week in cal['weeks'] for day in week['contributionDays']]
            months = monthly_counts(days, now)
    return {'schema_version': 2, 'account': metadata['login'],
            'updated_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'year': now.year,
            'joined': metadata['createdAt'][:10],
            'public_repositories': metadata['publicRepositories']['totalCount'],
            'stars_earned': stars, 'followers': metadata['followers']['totalCount'],
            **summarize(rows, now.year), 'annual': rows, 'monthly_contributions': months,
            'scope': 'GitHub-visible contribution history. Shared private activity is included only as anonymous contribution totals; it is never added to commit totals.'}


def card(value, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="250" height="114" viewBox="0 0 250 114" role="img" aria-label="{escape(label)}: {value:,}">
<rect width="250" height="114" rx="8" fill="#241D19"/>
<text x="20" y="53" fill="#BFA58A" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="700">{value:,}</text>
<text x="20" y="86" fill="#FAF8F5" font-family="Arial, Helvetica, sans-serif" font-size="16">{escape(label)}</text>
</svg>\n'''


def render(data):
    cards = [('contributions-year', data['contributions_year'], f"{data['year']} contributions"),
             ('contributions-all-time', data['contributions_all_time'], 'All-time contributions'),
             ('commits-year', data['commits_year'], f"{data['year']} visible commits"),
             ('commits-all-time', data['commits_all_time'], 'All-time visible commits')]
    files = {f'assets/stat-{slug}.svg': card(value, label) for slug,value,label in cards}
    images = '\n'.join(f'  <img src="./assets/stat-{slug}.svg" alt="{escape(label)}: {value:,}" width="250" height="114" />' for slug,value,label in cards)
    block = f'''{START}
<p>
{images}
</p>

**{data['public_repositories']} public repositories** · **{data['stars_earned']} stars earned**

Contributions include publicly shared private activity. Commit totals cover contribution-eligible commits visible to the updater; private contributions are not counted as commits. All-time totals span the contribution years GitHub reports.
{END}'''
    return files, block


def refresh(root, login, now):
    # Fetch and validate everything before touching the last successful output.
    data = collect(login, now)
    files, block = render(data)
    readme_path = root / 'README.md'
    readme = readme_path.read_text()
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise RuntimeError('README must contain one profile-stats marker pair.')
    readme = re.sub(re.escape(START)+r'.*?'+re.escape(END), lambda _: block, readme, flags=re.S)
    files['README.md'] = readme
    files['brand/public-stats.json'] = json.dumps(data, indent=2)+'\n'
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix+'.tmp')
        temporary.write_text(content)
        temporary.replace(target)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default='FasHub')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = refresh(args.root, args.username, datetime.now(timezone.utc))
    print(json.dumps({key: result[key] for key in ('updated_at','contributions_year','contributions_all_time','commits_year','commits_all_time')}))
