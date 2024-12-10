import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from datetime import datetime
import json

class MoodTracker:
    """A class for a mood tracker that records mood entries in a DataFrame and saves them to a CSV file.

    Attributes: 
    df (pandas.DataFrame): A DataFrame that has columns ['name', 'date', 'mood', 'context', 'severity'] the stores mood entries.

    Methods: add_entry(), 
    Allows the user to input their mood entry details, validates inputs, and adds the
    entry to the DataFrame csv file called 'mood_data.csv'.
    """
    def __init__(self):
        """
        Initializes the MoodTracker instance with an empty DataFrame.

        Side Effects:
        Creates an empty DataFrame with columns ['name', 'date', 'mood', 'context', 'severity'].
        """
        self.df = pd.DataFrame(columns=['name', 'date', 'mood', 'context', 'severity'])

    def add_entry(self):
        """
        add_entry adds a new mood entry to the DataFrame and allows the user to input their mood entry details, validates inputs, and adds the
        entry to the DataFrame csv file called 'mood_data.csv'.

        Args:None

        Side Effects:
        - Allows the user to input their entries through the terminal.
        - Reads the existing 'mood_data.csv' file if their is an existing entry.
        - Creates or updates 'mood_data.csv' with the new entry.

        Returns: None
        """
        print("Welcome to your personal Mood Tracker!")
        name = input("Enter your name: ")
        date = input("Enter the date (YYYY-MM-DD): ")

        try: 
            datetime.strptime(date, "%Y-%m-%d")
        
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return
        
        mood = input("What mood are you feeling? (sad, happy, surprised, bad, fearful, angry, disgusted): ")

        valid_moods = ['sad', 'happy', 'surprised', 'bad', 'fearful', 'angry', 'disgusted']
        if mood not in valid_moods:
            print("Invalid mood entered. Please choose a valid mood.")
            return

        context = input("Why are you feeling this way? ")
        severity = input("On a scale of 1-10, how severe is this emotion? ")

        try:
            severity = int(severity)
        except ValueError:
            print("Invalid severity. Please enter a number between 1 and 10.")
            return
        
        if not (1 <= severity <= 10):
            print("Severity must be between 1 and 10.")
            return

        new_entry = pd.DataFrame({
            'name': [name],
            'date': [date],
            'mood': [mood],
            'context': [context],
            'severity': [severity]
        })
        try:
            self.df = pd.read_csv('mood_data.csv')
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['name', 'date', 'mood', 'context', 'severity'])

        self.df = pd.concat([self.df, new_entry], ignore_index=True)

        self.df.to_csv('mood_data.csv', index=False)
        print(f"Entry for {name} on {date} saved successfully!")

    def view_entries(self):
        """
        Display all past entries from the CSV.
        """
        try:
            self.df = pd.read_csv('mood_data.csv')
            print("\nYour previous entries:")
            print(self.df)
        except FileNotFoundError:
            print("No past entries found. Please add an entry first.")

    def search_context_entries(self, keyword):
        """Allows user to search for a keyword in the context.

        Args:
            keyword (str): word user is searchin for

        Returns:
            strs: entries that contain the keyword

        Raises:
            Exception: Any error that may happen

        Author & Technique:
            Lita O'Brien, json.dumps()
        """
        try:
            self.df = pd.read_csv('mood_data.csv')
            matches = self.df[self.df['context'].str.contains(keyword, case=False, na=False)]
            
            if matches.empty:
                print(f"No entries match the context keyword '{keyword}'.")
            else:
                matches_json = json.dumps(matches.to_dict(orient="records"), indent=2)
                print(matches_json)
        except Exception:
            print(f"An error occurred: {Exception}")

    def describe_severity_from_csv(self):
            """
            Reads mood entries from CSV and generates a description of the severity for each entry.

            Returns:
                str: severity in word form on certain date.

            Raises:
                FileNotFoundError: file doesn't exist/can't find it.

            Author & Technique:
                Lita O'Brien, conditional expressions
            """
            try:
                self.df = pd.read_csv('mood_data.csv')
                if self.df.empty:
                    print("No mood entries found.")
                    return

                for index, row in self.df.iterrows():
                    severity = row['severity']
                    date = row['date']
                    
                    severity_word = (
                        "marginal" if severity <= 2 else
                        "slight" if severity <= 5 else
                        "enhanced" if severity <= 8 else
                        "moderate"
                    )
                    
                    print(f"You had {severity_word} feelings on {date}")
            
            except FileNotFoundError:
                print("File not found.")
    
    def plot_previous_entries(self):
        """
        Create a seaborn plot displaying the mood severity distribution for the last 3 mood entries.

        Attributes:
            df (pd.DataFrame): The DataFrame containing mood data read from the 'mood_data.csv' file.

        Side Effects:
            - Reads the 'mood_data.csv' file to load the mood data.
            - If there are fewer than 3 entries, all available entries will be plotted.
            - Displays a seaborn count plot showing the distribution of mood severity for the last 3 (or fewer) entries.
            - If the CSV file is not found, an error message is printed.

        Returns:
            None: The method does not return a value. It only generates and displays a plot.

        Raises:
            FileNotFoundError: If the 'mood_data.csv' file is not found.
        """
        try:
            self.df = pd.read_csv('mood_data.csv')
            if len(self.df) < 3:
                print("There are less than 3 entries. Showing all available entries.")
                data_to_plot = self.df
            else:
                data_to_plot = self.df.tail(3) 

            plt.figure(figsize=(8, 6))
            sns.countplot(data=data_to_plot, x='mood', hue='severity')
            plt.title('Mood Severity Distribution for Last Entries')
            plt.xlabel('Mood')
            plt.ylabel('Count')
            plt.show()
        except FileNotFoundError:
            print("No past entries found. Please add an entry first.")
            
    def __call__(self, analysis = "summary"):
        """
        Perform mood analysis on the data and return the result based on the specified analysis type.

        Args:
            analysis (str): The type of analysis to perform. 
                         Options are 'summary' or 'trend'. Default is 'summary'.
    
        Attributes:
            df (pd.DataFrame): The DataFrame containing mood data read from the 'mood_data.csv' file.

        Side Effects:
            - Reads the 'mood_data.csv' file to load the mood data.
            - If the file is not found, an error message is returned.
            - If the DataFrame is empty, an appropriate message is returned.

        Returns:
            str: A string summarizing the analysis results:
                - 'summary' analysis returns the total number of entries, the most common mood, and the average severity.
                - 'trend' analysis returns the distribution of mood counts.
                - An error message is returned if an invalid analysis type is provided or if the CSV file is not found.

        Raises:
            FileNotFoundError: If the 'mood_data.csv' file is not found.
        """
        try:
            self.df = pd.read_csv('mood_data.csv')
        except FileNotFoundError:
            return "csv file not found."
            
        if self.df.empty:
            return "No data to show."
        
        if analysis == "summary":
            return (
                f"Summary:\n"
                f"- Total Entries: {len(self.df)}\n"
                f"- Most Common Mood: {self.df['mood'].mode()[0]}\n"
                f"- Average Severity: {self.df['severity'].mean():.2f}"
            )
        elif analysis == "trend":
            mood_counts = self.df['mood'].value_counts()
            return f"mood trend: \n{mood_counts.to_string()}"
        else:
            return "Invalid analysis, use summary or trend."

def parse_args():
    """
    Parse command-line arguments and execute the appropriate action based on the user's input.

    Attributes:
        args (argparse.Namespace): The parsed command-line arguments containing the user's specified actions.

    Side Effects:
        - Creates an instance of the MoodTracker class.
        - Executes one of the following actions based on the parsed arguments:
          - `--add`: Adds a new mood entry by calling the `add_entry` method of the `MoodTracker` instance.
          - `--view`: Displays all previous mood entries by calling the `view_entries` method of the `MoodTracker` instance.
          - `--plot`: Plots the mood severity distribution for the last 3 entries by calling the `plot_previous_entries` method of the `MoodTracker` instance.
          - `--analysis`: Performs mood analysis (either 'summary' or 'trend') by calling the `__call__` method of the `MoodTracker` instance with the specified analysis type.
          - `--search`: Allows the user to search for mood entries by keyword in the context.
          - `--describe`: Allows user to see a word form of their rated severity.
    
    Returns:
        None: The function does not return any value. It directly performs actions based on the command-line arguments.
    
    Raises:
        argparse.ArgumentError: If invalid arguments are passed, such as missing or incorrect flag types.
    """
    parser = ArgumentParser(description="Mood Tracker")
    parser.add_argument('--add', action='store_true', help="Add a new mood entry")
    parser.add_argument('--view', action='store_true', help="View previous mood entries")
    parser.add_argument('--plot', action='store_true', help="Plot the last 3 mood entries")
    parser.add_argument('--analysis', type=str, help="Perform mood analysis: summary or trend")
    parser.add_argument('--search', type=str, help="Search for mood entries by context keyword")
    parser.add_argument('--describe', action='store_true', help="Describes mood severity based on past entries")
    
    args = parser.parse_args()

    tracker = MoodTracker()
        if args.add:
            tracker.add_entry()
        elif args.view:
            tracker.view_entries()
        elif args.plot:
            tracker.plot_previous_entries()
        elif args.analysis:
            print(tracker(analysis=args.analysis))
        elif args.search:
            print(f"Searching for keyword in context: {args.search}")
            tracker.search_context_entries(args.search)
        elif args.describe:
            tracker.describe_severity_from_csv()
        else:
            print("No action specified. Use add, view entries, plot, analysis.")

if __name__ == "__main__":
    parse_args()
