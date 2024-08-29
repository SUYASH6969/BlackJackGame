""" SUYASH BHATT 
Welcome to the game of BlackJack
Details:
It  is a single player game against a dealer using a standard deck of card
Goal is to draw cards of total value higher than that of dealer but less than 21
Card Points
2	 2
3	 3
4 	 4..so on 
J	 10
Q	 10
K	 10
A	 11 or 1 (Value of Ace is 1 if the total points of cards in your hand goes over 21 otherwise,it is 11)
If total value is equal to 21,means its a BLACKJACK and a straight win
If both the player and dealer hits BLACKJACK, Dealer wins
The game begins with two cards each for Player and the Dealer.
Both cards of the player would be shown while for Dealer, second card would be hidden
Now the player has two choices;
1)Hit ie, to accept more cards if he thinks his total is less than the total value of dealer cards
2)Stand ie to pass it over if he thinks he has got total higher than that of the dealer
Remember,if you "Hit" for more cards and total reaches more than 21, you 'BUST' meaning you lose.
After the Stand button is pressed, Dealer cards will be drawn by the python program .
Dealer has to keep drawing more cards until his total reaches atleast 17.
If total value of  dealer cards reaches more than 21, he 'BUSTS' or loses 
If total value of player and dealer cards is equal but less than 21, Its a "TIE"

class BLACKJACKGUI will be called first to run GUI which will command class Blackjack to run the game. 
Blackjack game will ask class Player and class Dealer to play .
To draw cards,class Deck and class Card will be used.
Since this program utilises OOP, classes should inherit objects of the parent class according to need

**IMPORTANT**
Now since this is a GUI program, implementation needs virtual cards which is present in a folder called DECK.
Project opened in any IDE should conatin both backjackgui.py and folder DECK. 

"""

from tkinter import *#importing GUI library
import random


class Blackjack(object): #main class to obtain cards of player and the dealer and print results
	
	def __init__(self):
		self.deckobj = Deck()#Deck class is called to obtain a  deck 
		self.deckobj.shuffle()
		
		#Pass the player and the dealer two cards each
		self.player = Player([self.deckobj.deal(), self.deckobj.deal()])
		self.dealer = Dealer([self.deckobj.deal(), self.deckobj.deal()])

	def getplayercards(self):
		"""Returns a list of the player's cards."""
		return self.player.getcards()
		
	def getdealercards(self):
		"""Returns a list of the dealer's cards."""
		return self.dealer.getcards()
		
	def player_hit(self):
		"""Deals a card to the player. Returns a tuple output of the card and the player's score."""
		card = self.deckobj.deal()
		card.turn()
		self.player.hit(card)
		return (card, self.player.getscore())
		
	def dealer_hit(self):
		"""Deals cards to the dealer until an outcome occurs. Returns a string representing the outcome."""
		self.dealer.turnfirstcard()
		playerscore = self.player.getscore()
		if playerscore > 21:
			return "PLAYER BUSTS.PLAYER LOSE!"
		else:
			self.dealer.hit(self.deckobj)
			dealerscore = self.dealer.getscore()
			if dealerscore > 21:
				return "DEALER BUSTS.PLAYER WINS!"
			elif dealerscore > playerscore:
				return "DEALER WINS"
			elif dealerscore < playerscore and playerscore <= 21:
				return "PLAYER WINS!"
			elif dealerscore == playerscore:
				if self.player.Blackjackhand() and not self.dealer.Blackjackhand():
					return "PLAYER BLACKJACK.PLAYER LOSE!"
				elif not self.player.Blackjackhand() and self.dealer.Blackjackhand():
					return "DEALER BLACKJACK.PLAYER LOSE!"
				else:
					return "ITS A TIE"

					
class Card(Blackjack):
	""" Class to list suit and rank in a standard deck"""

	rank_list = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

	suit_list = ('Spades', 'Hearts', 'Diamonds', 'Clubs')

	back_face = 'DECK/b.gif'

	def __init__(self, rank, suit):
		"""Creates a card of given suit and rank and connects it to its corresponding image"""
		self.rank = rank
		self.suit = suit
		self.file_name = 'DECK/' + str(rank) + suit[0].lower() + '.gif'
		self.faceup = False #default value of faceup is false which means back of the card will be shown
	
	def turn(self):
		"""Turns the face of the card"""
		self.faceup = not self.faceup #turns the face of the card 
		
	def file_name1(self):
		"""Returns the image corresponding to card if face up  or else,returns blank if face is down"""
		if self.faceup:
			return self.file_name
		else:
			return Card.back_face #stores back image of the card
        
	def __str__(self):
		"""Returns string representation  of the hand """
		if self.rank == 1: #points associated with each rank
			rank = 'Ace'
		elif self.rank == 11:
			rank = 'Jack'
		elif self.rank == 12:
			rank = 'Queen'
		elif self.rank == 13:
			rank = 'King'
		else:
			rank = self.rank
		return str(rank) + ' of ' + self.suit

class Deck(object):
	""" Creates a standard deck of 52 cards"""

	def __init__(self):
		"""Creates deck of cards"""
		self.hand = [] #creating a deck and storing it in hand
		for suit in Card.suit_list:
			for rank in Card.rank_list:
				c = Card(rank, suit)
				self.hand.append(c)

	def shuffle(self):
		"""Shuffles the deck"""
		random.shuffle(self.hand)

	def deal(self):
		"""Pops the top card unless the deck is empty"""
		if len(self) == 0:
			return None
		else:
			return self.hand.pop(0)

	def __len__(self):
		"""Returns number of cards left in the deck"""
		return len(self.hand)

	def __str__(self): 
		"""Returns the string representation of a deck."""
		self.result = ''
		for c in self.hand:
			self.result = self.result + str(c) + '\n'
		return self.result


#from cards import Deck, Card 


class Player(Deck,Card):
	"""This class represents a player in a blackjack game."""
	
	def __init__(self, cards):
		self.hand = cards
		for card in self.hand:
			card.turn()

	def __str__(self):
		"""Returns string rep of cards and points."""
		string = ", ".join(map(str, self.hand))
		string += "\n  " + str(self.getscore()) + " points"
		return string
		
	def hit(self, card):
		self.hand.append(card) #append to card in the hands of player
		
	def getscore(self):
		"""Returns the number of points in the hand"""
		total = 0
		for card in self.hand:
			if card.rank > 9:
				total += 10
			elif card.rank == 1:
				total += 11
			else:
				total += card.rank
		#Deduct 10 if value greater than 21 
		for card in self.hand:
			if total <= 21:
				break
			elif card.rank == 1:
				total -= 10
		return total
		
	def Blackjackhand(self):
		"""if total value is 21, its BLACKJACK"""
		return len(self.hand) == 2 and self.getscore() == 21
		
	def getcards(self):
		return self.hand #gives the card to hands of the object

class Dealer(Player):
	"""Class Dealer contains his cards"""
	
	def __init__(self, cards):
		"""Initially,only one card of the dealer would be shown"""
		Player.__init__(self, cards)
		self.showfirstcard = True
		self.hand[0].turn() #turns the face of the first card
		
	def __str__(self):
		"""Shows only one card until Dealer has to hit."""
		if self.showfirstcard:
			return str(self.hand[0])
		else:
			return Player.__str__(self)
			
	def hit(self, deck):
		"""Add cards while points < 17, then allow all to be shown."""
		while self.getscore() < 17: #dealer has to keep accepting cards until its total is atleast 17 
			card = deck.deal()
			card.turn()
			self.hand.append(card)
			
	def turnfirstcard(self):
		"""Turns over the first card to show it"""
		self.showfirstcard = False 
		self.hand[0].turn()




class BlackJackGUI(Frame): #this class is for GUI 

	def __init__(self):
		Frame.__init__(self)
		self.master.title("Blackjack")
		self.grid()
		
		#Initializing buttons
		self.hit_button = Button(self, text = "Hit", bg="skyblue" ,command = self.hit) # button for Hit command 
		self.hit_button.grid(row = 0, column = 0)
		
		self.stand_button = Button(self, text = "Stand" , bg="skyblue" ,command = self.Stand) #button for stand command
		self.stand_button.grid(row = 0, column = 1)
		
		self.newgamebutton = Button(self, text = "New Game", bg="skyblue" , command = self.new_game) #button for new game
		self.newgamebutton.grid(row = 0, column = 2)
		
		#Status bar to print result
		self.status_var = StringVar()
		self.status = Entry(self, textvariable = self.status_var ,width=50) 
		self.status.grid(row = 1, column = 0, columnspan = 3)
		
		#Area pane for player and dealer cards
		self.player_pane = Frame(self)
		self.player_pane.grid(row = 2, column = 0, columnspan = 3)

		self.status_var1 = StringVar()
		self.status = Entry(self, textvariable = self.status_var1 ,width=50) 
		self.status.grid(row = 3, column = 0, columnspan = 3)

		self.dealer_pane = Frame(self)
		self.dealer_pane.grid(row = 4, column = 0, columnspan = 3 )
		self.new_game()
		
	# New Game
	def new_game(self):
		"""Instantiates the model and establishes the GUI"""
		self.model = Blackjack()
		
		#Refereshes the card area
		#Player Cards
		#increases the player pane if more cards are drawn
		self.player_image = list(map(lambda x: PhotoImage(file = x.file_name1 ()), self.model.getplayercards())) 
		self.player_label = list(map(lambda k: Label(self.player_pane, image = k), self.player_image))
		for col in range(len(self.player_label)):
			self.player_label[col].grid(row = 0, column = col)
			
		#Dealer Cards
		#increases the dealer pane if more cards are drawn	
		self.dealer_image = list(map(lambda x: PhotoImage(file = x.file_name1()), self.model.getdealercards()))
		self.dealer_label = list(map(lambda k: Label(self.dealer_pane, image = k), self.dealer_image))
		for col in range(len(self.dealer_label)):
			self.dealer_label[col].grid(row = 0, column = col)
			
		#Undisable the button and refresh the status variable when its a new game
		self.hit_button["state"] = NORMAL
		self.stand_button["state"] = NORMAL
		self.status_var.set("")
		self.status_var1.set("")
	
		
	def hit(self):
		"""Updates Card  Pane after hit function is called until value of cards reaches 21 ."""
		(card, points) = self.model.player_hit()
		card_image = PhotoImage(file = card.file_name1()) 
		self.player_image.append(card_image)
		label = Label(self.player_pane, image = card_image)
		self.player_label.append(label)
		label.grid(row = 0, column = len(self.player_label) - 1)
		self.status_var1.set(points)
		if points >= 21:
			self.Stand()   #Passes the control to dealer
			
	def Stand(self):
		"""Updates Card pane for the dealer and displays his card until value reaches 21"""
		self.hit_button["state"] = DISABLED #buttons should be disabled after the player cant draw any more cards
		self.stand_button["state"] = DISABLED
		
		#Dealer hit and refreshes the game
		result = self.model.dealer_hit()
		self.dealer_image = list(map(lambda x: PhotoImage(file = x.file_name1()), self.model.getdealercards()))
		self.dealer_label = list(map(lambda k: Label(self.dealer_pane, image = k), self.dealer_image))
		for col in range(len(self.dealer_label)):
			self.dealer_label[col].grid(row = 0, column = col)
		self.status_var.set(result)
		
def main():
	BlackJackGUI().mainloop() #calls the main function of the GUI 

main()









	






