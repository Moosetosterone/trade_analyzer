# 1. Switch to develop
git checkout develop

# 2. Pull latest changes (if working with a remote team)
git pull origin develop

# 3. Merge sprint3 into develop
git merge --no-ff sprint3 -m "Merge sprint3: add reporting & export utilities"

# 4. Push the updated develop branch
git push origin develop


git branch -d sprint3
git push origin --delete sprint3




# create analytics/visualization.py from data/visualization.py
git mv data/visualization.py analytics/visualization.py

# remove now-empty data/ directory if it has no other files
rmdir data

# update imports across the repo:
grep -Rl "data.visualization" -e . | xargs sed -i '' 's|data.visualization|analytics.visualization|g'

# commit the change
git add .
git commit -m "refactor: move plot_equity_curve into analytics.visualization"



