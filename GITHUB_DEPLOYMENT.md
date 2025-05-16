# Deploying to GitHub

This guide provides step-by-step instructions for deploying your Django e-commerce project to GitHub.

## Prerequisites

- [Git](https://git-scm.com/downloads) installed on your local machine
- [GitHub account](https://github.com/join)
- GitHub CLI (optional, for easier authentication)

## Steps to Deploy to GitHub

### 1. Initialize a Git Repository (if not already done)

Open a terminal/command prompt in your project root directory and run:

```bash
git init
```

### 2. Add Files to Git

Stage all files that should be included in your repository:

```bash
git add .
```

This will add all files except those specified in the `.gitignore` file.

### 3. Commit Your Changes

Create your first commit:

```bash
git commit -m "Initial commit"
```

### 4. Create a New Repository on GitHub

1. Go to [GitHub](https://github.com/) and sign in
2. Click on the "+" icon in the top-right corner and select "New repository"
3. Enter a repository name (e.g., "ecommerce-django")
4. Add an optional description
5. Choose whether the repository should be public or private
6. Do NOT initialize the repository with a README, .gitignore, or license
7. Click "Create repository"

### 5. Connect Your Local Repository to GitHub

After creating the repository, GitHub will display commands to connect your local repository. Use the commands under "…or push an existing repository from the command line":

```bash
git remote add origin https://github.com/yourusername/ecommerce-django.git
git branch -M main
git push -u origin main
```

Replace `yourusername` with your actual GitHub username and `ecommerce-django` with your repository name.

### 6. Verify the Deployment

1. Refresh your GitHub repository page
2. You should see all your project files and directories

## GitHub Actions (CI/CD)

This project includes a GitHub Actions workflow file (`.github/workflows/django.yml`) that automatically runs tests when you push to the main branch or create a pull request.

To view the workflow:
1. Go to your GitHub repository
2. Click on the "Actions" tab
3. You'll see the workflow runs listed there

## Making Changes and Updates

After the initial deployment, you can make changes to your code and push them to GitHub:

1. Make your changes to the code
2. Stage the changes:
   ```bash
   git add .
   ```
3. Commit the changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to GitHub:
   ```bash
   git push
   ```

## Branching Strategy (Optional)

For a more organized development workflow:

1. Create a new branch for each feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
2. Make your changes and commit them
3. Push the branch to GitHub:
   ```bash
   git push -u origin feature-name
   ```
4. Create a Pull Request on GitHub to merge your changes into the main branch

## Troubleshooting

### Authentication Issues

If you encounter authentication issues:

1. Use GitHub CLI for authentication:
   ```bash
   gh auth login
   ```
2. Or set up SSH keys for GitHub:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   Then add the public key to your GitHub account.

### Large Files

If you have large files that exceed GitHub's file size limit:
1. Add them to `.gitignore`
2. Or consider using [Git LFS](https://git-lfs.github.com/) for large files

## Additional Resources

- [GitHub Documentation](https://docs.github.com/en)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)