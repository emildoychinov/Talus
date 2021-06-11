# Talus
 <img src="https://media.discordapp.net/attachments/761478365046767626/852988520540405800/pixil-frame-0_1.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
     
     
Talus is a Discord bot written in Python.
Talus serves as my project for the "Scripting languages" class at TUES

## Who is Talus intended for?

Talus is intended for all the people that use discord and want a unique and interesting experience.

## How is Talus 'unique'?

Talus is unique in many ways. Unlike other discord bots it can speak to you (well, sort off), solve mathematical expressions, beat you in a game of Tic Tac Toe and even help you with the moderation of your server!
 
# Talus posseses commands for different needs.
  
   ## There is a mathematical parser 
  It is a recursive descent parser which is shortly yet effectively and elegantly written. It can solve any PEMDAS equation you like. 
  
   ## As said earlier, Talus can talk to you. 
   <img src="https://cdn.discordapp.com/attachments/757618149272191099/852103807189778432/unknown.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
     
     
  This is done via a seq2seq algorithm that is set up on a encoder-decoder LSTM model. The loss it uses is categorical crossentropy.  And the method of teaching that is used is teacher forcing (the technique where the target word is passed as the next input to the decoder in short). Talus is not the most intelligent bot, but when given a good dataset and more epochs of learning, it can reach a good accuracy.

  ## Talus can play Tic Tac Toe with you
  Talus uses a full tree search minimax algorithm in order to be able to play as good as possible versus an oponent. For a new inexperienced user the nature of this algorithm could be confusing, since there are instances where the bot will pick a move that results in a draw even though it has an obvious move for a win. That happens because the aim of the algorithm is not just to win but to minimize the chances of losing and thus maximise the chances of winning. In other words, a normal draw is more preferable to a risky win. 

# Don't know how to use the bot?

```yaml
~help (to see the list of all commands)
~help <command> (to see information about a specific command)
```

# What's next?

Even though Talus is a project, as mentioned earlier, I fully intend to continue working on it and make the bot as good as it can possibly get.

# License
[MIT](https://choosealicense.com/licenses/mit/)
