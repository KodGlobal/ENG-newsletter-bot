# Newsletter Bot

### Commands:

- **!news**: Retrieves and displays news from a specified RSS feed.
- **!subscribe**: Allows a user to subscribe to notifications by keyword.
- **!unsubscribe**: Allows a user to unsubscribe from notifications by keyword.
- **!notifications**: Displays the user's current subscriptions.
- **!latest**: Shows the latest news for all of the user's subscriptions.
- **!info**: Displays information about the bot.

### Background Task:

**update_news**: Updates news every 10 minutes and caches them if the news headline contains a keyword from the subscriptions.

### Data Structure:

**subscriptions**: A dictionary for storing user subscriptions.  
**news_cache**: A cache for storing news related to keywords.

### RSS Parser:

Uses the **feedparser** library to fetch news from RSS feeds.