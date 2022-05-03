# Rexter

[Rexter](https://twitter.com/McocBot) is a Twitter Bot whoch retweets and likes all tweets related to MCoC.

## Usage

You can just tweet by mentioning the Official Twitter Handle of either [Rexter](https://twitter.com/McocBot) itself or of the [Contest of Champions](https://twitter.com/MarvelChampions). You can also mention any of the following-

- #ContestofChampions
- #MCoC

## Self-Hosting

To self host the Bot, do the following.

- Clone the repo.

  - ```bash
    git clone https://github.com/Rexians/Rexter.git
    ```

- Create a Twitter Bot

  - Create a Twitter Developer Account [here](https://developer.twitter.com/).
  - Create a project and an app in it.
  - Apply for Elevated Access.
  - Enable OAuth 2.0 and 1.0a with read and write permissions.
  - Generate Access Key and Token for the app created above.
  - Copy all the details including Consumer Keys and Authentication Tokens.

- Create a .env

  - Add all the tokens and keys like this:

  ```env
  API_KEY =
  API_KEY_SECRET =
  ACCESS_TOKEN =
  ACCESS_TOKEN_SECRET =
  BEARER_TOKEN =
  CLIENT_ID =
  CLIENT_SECRET =
  ```

- Install [Tweepy](https://github.com/tweepy/tweepy) module:

  - ```bash
    pip install tweepy
    ```

- Run the app.py

## Contributing

For contribution guidelines please refer to the [Contributing.md](CONTRIBUTING.md)
