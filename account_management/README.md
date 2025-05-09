@VERA I've restructured some of the account management logic
- The original AuthenticationSession did not authenticate anything, it just created a session. I've added a new class called AuthenticationSession that handles the authentication process.
- What we first called AuthenticationSession is now called LoginSession. It creates a session and handles the session logic.

