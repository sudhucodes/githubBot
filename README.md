# GitHub Streak Tracker Bot

This Python-based bot automates the process of committing changes to a GitHub repository. It tracks changes and logs them with timestamps in a `streak_tracker.txt` file, pushing them to your GitHub repository. The bot uses a JSON file to store commit messages and their corresponding changes, ensuring that commits are not repeated.

## Features

- Appends timestamps to a tracking file (`streak_tracker.txt`) in your repository.
- Commits changes with messages stored in a JSON file.
- Pushes the commits to your GitHub repository.
- Logs each operation to a file (`github_bot.log`) for troubleshooting.
- Supports handling multiple commits stored in a JSON file.

## Prerequisites

Before using this bot, ensure the following:

- Python 3.7 or later
- Python packages: `pygit2`, `python-dotenv`, and `logging`
- A GitHub account with a repository to track
- A personal access token for GitHub (with `repo` permissions)
- PythonAnywhere account (for deployment)

## Installation

1. Clone this repository or download the code.
2. Install the required Python packages:

   ```bash
   pip install pygit2 python-dotenv
   ```

3. Create a `.env` file in the root of your project directory. Add your GitHub username and personal access token:

   ```plaintext
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_github_token
   ```

4. Create a `commit_data.json` file in the root of your project directory. This file will contain the commit messages and the corresponding changes to be logged.

   Example `commit_data.json`:

   ```json
   {
       "commits": [
           {
               "message": "Added a new timestamp entry to the streak tracker",
               "change": "Appended the current timestamp to the streak_tracker.txt file to ensure continuous tracking of commit history."
           },
           {
               "message": "Refined streak tracker with improved formatting",
               "change": "Updated the streak_tracker.txt file with consistent formatting to enhance readability and structure."
           }
       ]
   }
   ```

5. The `streak_tracker.txt` file will automatically be created and updated with each commit.

## Usage

1. Run the Python script to commit changes:

   ```bash
   python main.py
   ```

2. The bot will:

   - Read the `commit_data.json` file for commit messages and changes.
   - Append the change (with timestamp) to `streak_tracker.txt`.
   - Commit the change to the GitHub repository.
   - Push the changes to the remote repository.
   - Log the action in `github_bot.log`.

3. You can check the log file (`github_bot.log`) for details about each operation.

## Deploying on PythonAnywhere

You can deploy this bot to PythonAnywhere to run it periodically.

### Steps:

1. **Create a PythonAnywhere Account**: If you don’t have one already, [sign up](https://www.pythonanywhere.com/).

2. **Upload the Code**: 
   - After logging in, go to the **Files** tab.
   - Upload your Python script (`main.py`), `.env`, and `commit_data.json` files to your PythonAnywhere file system.

3. **Set Up a Virtual Environment**:
   - Open a Bash console in PythonAnywhere and create a virtual environment:
     ```bash
     python3 -m venv github_bot_env
     source github_bot_env/bin/activate
     ```
   - Install the required packages:
     ```bash
     pip install pygit2 python-dotenv
     ```

4. **Schedule the Bot to Run Automatically**:
   - Go to the **Tasks** tab on PythonAnywhere.
   - Add a new scheduled task to run your script at your desired interval (e.g., every hour). For example, you can use the following command:
     ```bash
     python /home/yourusername/path_to_your_script/main.py
     ```

5. **Environment Variables**:
   - You can add your `.env` file using the **Files** tab, or you can set environment variables directly in PythonAnywhere's Bash console:
     ```bash
     export GITHUB_USERNAME="your_github_username"
     export GITHUB_TOKEN="your_github_token"
     ```

6. **Logs**: PythonAnywhere provides logs for scheduled tasks, so you can monitor the output of your script by checking the logs in the **Tasks** tab.

## Author Details

- **Author**: [SudhuCodes](https://github.com/sudhucodes)
- **Project**: GitHub Streak Tracker Bot
- **License**: MIT License

## Troubleshooting

- **Error reading or writing to JSON file**: Ensure that the `commit_data.json` file is correctly formatted and accessible.
- **Push fails**: Make sure your GitHub token has the appropriate `repo` permissions for both public and private repositories.
- **Permission errors**: Ensure that the `.env` file is correctly set up with valid GitHub credentials.
- **Missing dependencies**: If the script complains about missing libraries, make sure you have installed the required Python packages (`pygit2`, `python-dotenv`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.