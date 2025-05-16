# PowerShell script to create git commits from a TSV file
Write-Host "Starting to create Git history from commits.local.tsv.txt"

# Check if the commits file exists
if (-not (Test-Path "commits.local.tsv.txt")) {
    Write-Host "Error: commits.local.tsv.txt not found!"
    Exit 1
}

# Make sure the git repo is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository"
    git init
}

# Reset to a clean state
git checkout --orphan temp_branch
git add -A
git commit -m "Initial commit"
git branch -D main 2>$null
git branch -m main

# Read the commits file and process each line
$commits = Get-Content "commits.local.tsv.txt" | Where-Object { $_ -notmatch "^// filepath:" }

foreach ($line in $commits) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    
    $parts = $line -split "`t"
    if ($parts.Count -lt 4) { continue }
    
    $hash = $parts[0]
    $author = $parts[1]
    $date = $parts[2]
    $message = $parts[3]
    
    Write-Host "Creating commit: $message"
    
    # Format date for Git
    $env:GIT_AUTHOR_DATE = $date
    $env:GIT_COMMITTER_DATE = $date
    
    # Create empty commit with the message
    git commit --allow-empty -m $message --author="$author <$author@example.com>"
    
    Write-Host "Created commit with message: $message"
}

Write-Host "Git history creation complete. Run 'git log' to see the commits."

# Optional: Push to remote repository if desired
# git push -f origin main
