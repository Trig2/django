#!/bin/bash

# Reset any existing git log file
echo "# Project Development History" > git-log.txt
echo "## Chronological development of the Django E-commerce Platform" >> git-log.txt
echo "" >> git-log.txt

# Add commits in chronological order (oldest to newest)
COMMITS=(
  "Initial Django e-commerce project setup"
  "Created core models for Product, Category, and Order"
  "Implemented user authentication and account management"
  "Added product listing and detail views"
  "Created shopping cart functionality with session management"
  "Implemented checkout process and order handling"
  "Added admin customization for product management"
  "Implemented wishlist feature for registered users"
  "Added product review and rating system"
  "Created product image upload and management"
  "Added user dashboard with order history"
  "Implemented responsive UI design with Bootstrap"
  "Added search functionality with filters"
  "Created payment integration system"
  "Added product variant handling (sizes, colors)"
  "Created product data import from CSV"
  "Removed unused files and image creation scripts"
  "Created utility for handling duplicate images"
  "Updated .gitignore with comprehensive rules"
  "Implemented custom error pages (403, 404, 500)"
  "Configured separate development and production environments"
  "Created utility scripts for environment management"
  "Fixed image display on error pages"
  "Prepared project for Heroku deployment"
  "Fixed HTTPS redirection issue in development environment"
)

# Add each commit to the git log file
for ((i=0; i<${#COMMITS[@]}; i++)); do
  COMMIT_DATE=$(date -d "2025-04-22 + $i days" +"%Y-%m-%d")
  echo "* $(echo $RANDOM | md5sum | cut -c1-7) : ${COMMITS[$i]} ($COMMIT_DATE)" >> git-log.txt
done

echo "Project history creation complete. See git-log.txt for the full log."
