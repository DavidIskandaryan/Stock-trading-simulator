#imports everything from tkinter
from tkinter import *
#gives a name to tkinter to be referenced to later
import tkinter as tk
#the api that lets me get the data on a given date of the stock price
import alpaca_trade_api as tradeapi
#librery for plotting graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#time librery used for halting the program for some time when needed
import time
#threading used for switching from running one function to another
import threading
#used for logging in the dictonarys to be used for the leaderboard
import pickle
#more imports from alpaca API 
from alpaca_trade_api.rest import TimeFrame
#import that lets you display a text widjets with scrollable feature
import tkinter.scrolledtext as st



apikey = "PKSCR3CZ22BE7I53O5WS"
seckey = "xRVNb0PdHO7v2OmNx0HRAWF8wqwS2e6zKUjvl1oo"
#API endpoint URL
url = "https://paper-api.alpaca.markets"
#api_version v2 refers to the version that we'll use
api = tradeapi.REST(apikey, seckey, url, api_version='v2')
# Stock movment timeframe is from week_start to week_end.
week_start = "2016-01-01"
week_end = "2016-01-07"



#algorithm for changing the month and year when needed after moving the days in the string
def change_month(day, year, month):
    #moves the year part of the string when reached 12 monthes
    if (month == '12'):
        year = str(int(year) + 1)
        month = '01'
        day = '01'
    else:
        #moves monthes when it reaches 10 
        if (int(month) >= 9):
            month = str(int(month) + 1)
            day = '01'
        else:
        #moves months when below 10 since it needes to be in 0 followed by a number format
            month = month[0] + str(int(month[1]) + 1)
            day = '01'
    return day, year, month


  
#algorithm for moving the day part in the string
def move_days(date_split):
    #splits the string up for separate strings for day, month, year
    day = date_split[-2] + date_split[-1]
    month = date_split[-5] + date_split[-4]
    year = date_split[0] + date_split[1] + date_split[2] + date_split[3]
    #creates list of months with 30 days and list of monts with 31 days
    list_30 = ['04', '06', '09', '11']
    list_31 = ['01', '03', '05', '07', '08', '10', '12']
    #system for cheacking what type of month it is if its not in both lists it February
    if (month in list_30):
        if (int(day) != 30):
        #depending if the day has 0 at the start or not it needs to be moved differently
            if (int(day) >= 9):
                day = str(int(day) + 1)
            else:
                day = day[0] + str(int(day[1]) + 1)
        #once it reaches end of the days in the month it calls too the change_month function to change the month and set the day to 01 
        if (int(day) == 30):
            day, year, month = change_month(day, year, month)
    elif (month in list_31):
        #does the same thing it did with 30 days
        if (int(day) != 31):
            if (int(day) >= 9):
                day = str(int(day) + 1)
            else:
                day = day[0] + str(int(day[1]) + 1)
        if (int(day) == 31):
            day, year, month = change_month(day, year, month)
    else:
        #if its February we check for a leap year when the year divisable by 100 it is not a leap year unless it divisable by 400
        the_year = int(year)
        #cheaks for divisabililty by 4, 100, 400
        mod_4 = the_year % 4
        mod_100 = the_year % 100
        mod_400 = the_year % 400
        #if its not divisable by 4 or 400 or if its divisable by 100 and not divisable by 400 then its not a gap year and the month has 28 days
        if ((mod_4 >= 1) or (mod_400 >= 1) or (mod_100 == 0 and mod_400 >= 1)):
          #same system for moving every other month exept the limit is 28
            if (int(day) != 28):
                if (int(day) >= 9):
                    day = str(int(day) + 1)
                else:
                    day = day[0] + str(int(day[1]) + 1)
            if (int(day) == 28):
                day, year, month = change_month(day, year, month)
            #if its divisable by 4 and not by 100 unless in a case of 400 its a leap year
            elif ((mod_4 >= 0 and mod_100 >= 1 ) or (mod_400==1)):
                #same system for moving every other month exept the limit is 29
                if (int(day) != 29):
                    if (int(day) >= 9):
                        day = str(int(day) + 1)
                    else:
                        day = day[0] + str(int(day[1]) + 1)
                if (int(day) == 29):
                    day, year, month = change_month(day, year, month)
    #reasambles the day, month, year in the format that the API understands
    date_split = year + "-" + month + "-" + day
    return date_split
#sets AI outcome as 1000000 as a starting point of the balance avalable for AI
AI_outcome=100000



#class for the AI
class AI():
    def __init__(self):
        #list of dates as they move they get appended to the list
        self.AI_x_points = []
        #list of number of weeks passed in that moment, in self.AI_x_points values will get appended to this list later on
        self.AI_y_points = []
        #the intial balance of the AI
        self.AI_initial_balance = 100000
        #profit or loss + funds
        self.AI_outcome = 100000
        #funds of the AI
        self.AI_balance = 100000
        #number of shares held by the AI
        self.AI_shares_held = 0
        #list of proportions of increased or decresed values of the balance
        self.AI_outcome_list=[1]
        #seperate list that is AI_outcome_list's last 10 values that where appendeded to it
        self.Machine_learning_list=[]
        #the proportion of the balance that should be invested
        self.AI_Balance_presentage=0.5

      
    #investment proportion change to AI_balance_presentage generator function
    def inv_generator(self):
      #generates an average of all values in self.Machine_learning list
      sum=0
      #adds every value in self.Machine_learning_list to sum
      for i in range(len(self.Machine_learning_list)):
        sum+=self.Machine_learning_list[i]
      #devides sum by the lists length to generate and avrage
      average=sum/(len(self.Machine_learning_list))
      return average


      
      '''val=self.Machine_learning_list.pop()
      if(len(self.Machine_learning_list)==0):
        if(self.AI_Balance_presentage*inv>=1):
          self.AI_Balance_presentage=0.25
          inv=1
          return inv
        else:
          return inv
      else:
        if(val>=1):
          inv=inv*(1+(val-1)*((1/(len(self.AI_outcome_list)))*decay))
          decay=decay+1
          return self.inv_generator(inv, decay)
        else:
          inv=inv*(1-(val*((1/(len(self.AI_outcome_list)))*decay)))
          decay=decay+1
          return self.inv_generator(inv, decay)'''


      
    #algorithm for buying the stock for the AI
    def algorithm(self, x_points, y_points):
      #gets the current date in number of weeks passes since plotting started
      self.AI_x_points=x_points
      #gets the current price of the stock
      self.AI_y_points=y_points
      #makes a copy of outcome list for the AI and removes evrything other than the last 10 items that where appended to it
      self.Machine_learning_list=self.AI_outcome_list.copy()
      #reverses the list for the order to be from last to first to be appended in order to pop evrything other than the last 10
      self.Machine_learning_list.reverse()
      while(len(self.Machine_learning_list)>10):
        self.Machine_learning_list.pop()
      #applies a increase or decrese to AI_Balance_presentage based on the number generetaed by inv generator
      self.AI_Balance_presentage=self.AI_Balance_presentage*self.inv_generator()
      #you cant invest more than alll of your balance thsu there is a cheaker to make Balance presentage for the AI 1 at most if its over 1
      if(self.AI_Balance_presentage>1):
        self.AI_Balance_presentage=1
      #gets current price
      AI_buy_price = self.AI_y_points[-1]
      #Buy amount is the shares that are going to be bought which is the amount of money inveseted devided by the price
      AI_buy_amount = (self.AI_Balance_presentage*self.AI_balance) / self.AI_y_points[-1]
      #takes away the amount of money invested from balance which is buy amount times by the price
      self.AI_balance = self.AI_balance - (AI_buy_amount*AI_buy_price)
      #assignes shares held the value of AI_buy_amount
      self.AI_shares_held=AI_buy_amount
      #outcome is the current price multiplied by the shares held added to the balance this is the liquid money owned
      self.AI_outcome = int(self.AI_balance +(self.AI_shares_held * self.AI_y_points[-1]))
      #becouse AI_outcome needs to be tracked on screen ai_outcome needs to be a global variable
      global AI_outcome
      #assigns the global value for the ai outcome to self.AI_outcome value for the class
      AI_outcome=self.AI_outcome

      
      
    #function for selling the assets every week in order to make a new decesion on the amount that should be invested  
    def AI_sell(self, x_points, y_points):
      #gets the current date in number of weeks passes since plotting started
      self.AI_x_points=x_points
      #gets current price
      self.AI_y_points=y_points
      #liquifies assets by adding the product of shares held and current price to the balance
      self.AI_balance=self.AI_balance+(self.AI_y_points[-1]*self.AI_shares_held)
      #after selling the number of shares held is 0
      self.AI_shares_held=0
      #aoutcome list is the proportion of profit or loss made and is appended to the list eache time the AI sells
      self.AI_outcome_list.append(self.AI_balance/self.AI_outcome)


      
#graph class for the live plotting buy, sell, and all other functionalities for the user 
class graph:
    def __init__(self):
        #variable that changes state from not plotting to plotting in order to allow for actions to be preformed in betwween
        self.continuePlotting = False
        #list of number of weeks passed in that moment constantly being appended with every plot
        self.x_points = []
        #list of stock price values
        self.y_points = []
        #number of weeks since plotting started
        self.week_count = 0
        #boolean to cheack weather the desired date has been reached
        self.end_of_time = False
        #initial balance
        self.initial_balance = 100000
        #profit or loss + funds
        self.outcome = 100000
        #avalable funds
        self.balance = 100000  
        #number of shares held by the user
        self.shares_held = 0
        #whether you have sold or not is cheacked by this boolean
        self.sold = False
        #name of the stock being practiced on
        self.Stock_name = ""
        #the balance after the game is done
        self.trading_rekord=""
        #hash value for the hasing algorithm
        self.hash_value=""
        #name of the player
        self.player_name=""
        #variable that indicates whether a stock has been found for plotting or not
        self.valid_stock=False
        

      
    #main function that holds all other functions for plotting and user interface also displaying the Leaderboard
    def app(self):
        #creates a tkinter window 
        window =Tk()
        #spacifies that white is the background color for the window
        window.config(background='white')
        #window size
        window.geometry("1000x700")
        #variable to be later displayed on screen sygnifies users current liquid money
        textchange = StringVar()
        textchange.set(self.outcome)
        #variable to be later displayed on screen sygnifies the AI's current liquid money
        AI_textchange = StringVar()
        AI_textchange.set(AI_outcome)

      
      
        #function for hiding the stock name box, player name boxe, text thats says what to enter in each box,and the search button after the values have been recorded and display error messege if stock not found   
        def hide_me(button):
            #recordes the name entered by the user for the stock
            self.Stock_name = textBox_2.get("1.0", "end-1c")
            #list of avalable stocks in the API
            active_assets=api.list_assets(status='active')
            #checks wheather the stock is in the API's database of stocks
            self.valid_stock=False
            for i in active_assets:
              if i.symbol==self.Stock_name:
                self.valid_stock=True
                break
            #if its not in the database prints stock is not found in database and drops out of the function by returning nothing
            if not self.valid_stock:
              print("Stock is not found in database")
              return
            #records the player name entered by the user
            self.player_name = textBox_3.get("1.0", "end-1c")
            #pack_forget() hides the widgets
            button.widget.pack_forget()
            text_1.pack_forget()
            textBox_2.pack_forget()
            textBox_3.pack_forget()
            #changes the name of the tkinter window the the stock name entered by the user
            window.title(self.Stock_name)
        #label thats says where to enter the stock and player name
        text_1=Label(window, text="ENTER PLAYER AND STOCK NAME")
        text_1.pack()
        #text box for player name
        textBox_3 = Text(window, height=1, width=6)
        textBox_3.pack()
        #text box for stock name
        textBox_2 = Text(window, height=1, width=6)
        textBox_2.pack()
        #search button that records the data in the 2 boxes and hides itself,the boxes, and the label thats says to enter the names
        Search = Button(window, text="Search", bg="grey", fg="white")
        Search.bind('<Button-1>', hide_me)
        Search.pack()
        #new figure for matplotlin
        fig = Figure()

        #adds a sublot
        ax = fig.add_subplot(111)
        #labels for x and y axis
        ax.set_xlabel("Weeks")
        ax.set_ylabel("Price")
        #makes the subplot a grid
        ax.grid()

        #creates a canvas and specifies its master and where it belongs
        graph = FigureCanvasTkAgg(fig, master=window)
        graph.get_tk_widget().pack(side="top", fill='both', expand=True)

      
      
        #function that plots the graph and displayes the Leaderboard when done plotting
        def plotter():
            #makes the start and end date global variables
            global week_end
            global week_start
            #while needed to continue plotting
            while self.continuePlotting:
                #adds the number of the week since plotting has started to the x_points list
                self.x_points.append(self.week_count)
                #adds the starting price to the y_points list
                self.y_points.append(230.77)
                #while plotting has not reached the end date
                while (self.end_of_time == False):
                    #if reached the moment of the end date
                    if week_end == "2021-09-17":
                        #store the last value
                        self.trading_rekord=int(self.outcome)
                        #hashing algoithm the uses mid-square method, clashes are not a problem so there no system in place to avoid that
                        self.hash_value=int((((self.trading_rekord*self.trading_rekord)/1000000)-int((self.trading_rekord*self.trading_rekord)/1000000))*1000000)
                        #creates a dictonary that holds the values for score, name and the hash value 
                        main_dict ={"score": self.trading_rekord,"name": self.player_name,"key": self.hash_value}
                        #list of dictonaries
                        list_of_dict=[]
                        #loads the value last stored in Leaderboard.pkl unpickles it and assigns it to loaded_dict
                        with open('Leaderboard.pkl', 'rb') as f:
                          loaded_dict = pickle.load(f)
                        #assings the value of loaded_dict to list_of_dict
                        list_of_dict=loaded_dict
                        #adds the most recent dictonary created from the last game to list_of_dict
                        list_of_dict.append(main_dict)
                        #stores the value of list_of_dict in the Leaderboard.pkl instead of the value that is currently on there
                        with open('Leaderboard.pkl', 'wb') as f:
                          pickle.dump(list_of_dict, f)
                          #distroys every single widget currently in the window tkinter window
                          for widget in window.winfo_children():
                            widget.destroy()     
                        #list of scores from the list_of_dicts all dictonaries
                        value_list=[]
                        for i in range(len(list_of_dict)):
                          dict_value=list_of_dict[i]
                          value_list.append(dict_value["score"])
                        #merge sorts the values in value_list low to high
                        merge_sort(value_list)
                        #list of hashvalues
                        hash_list=[]
                        #hashes all values from the value list using the same mid_square method as before and adds them to the hashlist
                        for j in range(len(value_list)):
                          hash_value=int((((value_list[j]*value_list[j])/1000000)-int((value_list[j]*value_list[j])/1000000))*1000000)
                          hash_list.append(hash_value) 
                        #list to be displayed on the leaderboard
                        sorted_dict_list=[]
                        #finds the hashvalue in the list of dictonaries and appendes that dictonary to the sorted_dict_list
                        #keeps going threough the hashvalue list from start to finish and finds the values effecting creating a sorted list
                        for k in range(len(hash_list)):
                          temp_dict=next(item for item in list_of_dict if item["key"] == hash_list[k])
                          sorted_dict_list.append(temp_dict)
                          #removes the dictonary after appending it to the list to avoid appending the same list twice
                          list_of_dict.remove(temp_dict)

                        #label in the tkinter window that says Leaderboard
                        tk.Label(window, text = "Leaderboard", background = 'grey', foreground = "black").grid(column = 0, row = 0)
                        # Creating scrolled text area
                        # widget with Read only by disabling the state
                        text_area = st.ScrolledText(window, width = 30, height = 8, font = ("Times New Roman", 15))
                        text_area.grid(column = 0, pady = 10, padx = 10)
                        #reverses the order for it to be high to low
                        sorted_dict_list.reverse()
                        #empty string
                        Leaderboard_text=""
                        #adds name and score of players and keeps them in seperate rows from the dictonary list dictonaries
                        for i in range(len(sorted_dict_list)):                         
                          Leaderboard_text=Leaderboard_text+(sorted_dict_list[i]["name"]+"       "+str(sorted_dict_list[i]["score"])+"\n")
                        #inserts the text into the scrolled text area
                        text_area.insert(tk.INSERT, Leaderboard_text)
  
                        # Making the text read only
                        text_area.configure(state ='disabled')
                        
                        #shows the end of plotting
                        self.end_of_time = True
                    else:
                        #adds to the week count with each iteration
                        self.week_count += 1
                        #appends the weeks count to the list of week counts
                        self.x_points.append(self.week_count + 1)
                        #finds the stock based on its NASDAQ name using the API
                        barset = api.get_bars(self.Stock_name, TimeFrame.Day, week_start, week_end, adjustment='raw')
                        #gets the price at the start of the day
                        week_open = barset[0].o
                        #get the price at end of the day
                        week_close = barset[-1].c
                        #runs the algorithm for buying the stock by the AI
                        Stock_AI.algorithm(self.x_points,self.y_points)
                        #append the end of the day price to the list of stock prices through the weeks
                        self.y_points.append(week_close)
                        #gets current price whichis the last item in the list
                        current_price = self.y_points[-1]
                        #self.outcome is the liquid assets which is sum of the balance and the product of the current price and the number of shares held
                        self.outcome = int(self.balance +(self.shares_held * current_price))
                        #the text that needs to be displayed on the screen for the players outcome
                        textchange.set(str(self.outcome))
                        #the text that needs to be displayed on the screen for AI's outcome
                        AI_textchange.set(str(AI_outcome))
                        #makes the graph a grid
                        ax.grid()
                        #plots the graph
                        ax.plot(self.x_points, self.y_points, color='orange')
                        #draws on the graph
                        graph.draw()
                        #pauses for 0.1 seconds before continoung the plotting function
                        time.sleep(0.1)
                        #moves the days for week start and week end 7 times
                        for x in range(7):
                            #the new week start is the previous week end
                            week_start = move_days(week_start)
                            #new week end is 7 days away from the previous week end after the function is done
                            week_end = move_days(week_end)
                        #sells the sahres that the AI has
                        Stock_AI.AI_sell(self.x_points,self.y_points)
                        b.pack_forget()

                      
                      
        #merge sort algorithm for the list of values
        def merge_sort(myList):
          if len(myList) > 1:
            mid = len(myList) // 2
            left = myList[:mid]
            right = myList[mid:]
            # Recursive call on each half
            merge_sort(left)
            merge_sort(right)
            # Two iterators for traversing the two halves
            i = 0
            j = 0        
            # Iterator for the main list
            k = 0        
            while i < len(left) and j < len(right):
              if left[i] <= right[j]:
                # The value from the left half has been used
                myList[k] = left[i]
                # Move the iterator forward
                i += 1
              else:
                myList[k] = right[j]
                j += 1
              # Move to the next slot
              k += 1

            # For all the remaining values
            #both while loops assign the right value to the correct spot on the list
            while i < len(left):
              myList[k] = left[i]
              i += 1
              k += 1

            while j < len(right):
              myList[k]=right[j]
              j += 1
              k += 1


              
        #function for the user to buy stocks
        def buy():
            #the shares have not been sold
            self.sold = False
            #In case of pressing buy before game started do nothing
            if(len(self.y_points)==0):
              return
            #gets the buy price from the list of stock prices through the weeks
            buy_price = self.y_points[-1]
            #gets the amount entered in the textbox by the user
            InputValue = textBox.get("1.0", "end-1c")
            #Checks if its a string that can be number or not and prints incorrect format whenever it is text or symbol
            if not InputValue.isnumeric():
              print("Incorrect format")
              return
            #if the user has enough money to make the transaction
            if (buy_price * (int(InputValue) / self.y_points[-1]) <= self.balance and buy_price * (int(InputValue) / self.y_points[-1]) > 0):
                #add the number of shares the user wishes to buy
                self.shares_held = self.shares_held + (int(InputValue) / self.y_points[-1])
                #subtract the value invested from the balance
                self.balance = self.balance - int(InputValue)
            elif(buy_price * (int(InputValue) / self.y_points[-1]) > self.balance):
                #in the case of not having enough money print insufficent funds
                print("Insufficent funds")
            else:
                #in the case of words, symbols, 0 or a negative number print Incorrect format
                print("Incorrect format")
        #function for selling the users shares

      
              
        def sell():
            #In case of pressing sell before game started do nothing
            if(len(self.y_points)==0):
              return
            #gets the current price
            sell_price = self.y_points[-1]
            #gets the amount of money the user wants to get by selling
            InputValue = textBox.get("1.0", "end-1c")
            #Checks if its a string that can be number or not and prints incorrect format whenever it is text or symbol
            if not InputValue.isnumeric():
              print("Incorrect format")
              return
            #the amount being sold is the amount of money the user wants to get divided by the current price
            sell_amount = int(InputValue) / self.y_points[-1]
            #if the user has that many shares as he whishes to sell
            if (sell_amount <= self.shares_held and sell_amount >0):
                #reduce the number of shares by the wished amount
                self.shares_held = self.shares_held - sell_amount
                #add the liquidified money to the balance
                self.balance = self.balance + sell_amount * sell_price
            elif(sell_amount > self.shares_held):
                #in the case that the requested amount is more than the user has invested in to the stock display insufficent shares message
                print("Insufficent shares")
            else:
              #in the case of words, symbols of negative number print Incorrect format
              print("Incorrect format")            
            #after selling set sold to true
            self.sold = True

          
          
        #this function handles threading 
        def gui_handler():
            #In case of start being pressed before a stock is selected
            if(self.valid_stock==False):
              return
            #if the plotting is currently going on
            if self.continuePlotting == True:
                #halt it for now
                self.continuePlotting = False
            else:
                #if not continues plotting
                self.continuePlotting = True
            #thread that runs the function of plotting
            threading.Thread(target=plotter).start()


          
        #label for the users outcome
        outcome = Label(window, textvariable=textchange, bg='white').pack(side=RIGHT, padx=80, pady=0)
        #text that point to users balance
        Your_text= Label(window, text="Your balance:", bg='white').pack(side=RIGHT, padx=10, pady=0)
        #label for the AI's outcome
        AI_outcome_label = Label(window, textvariable=AI_textchange, bg='white').pack(side=RIGHT, padx=80, pady=0)
        #text that points to the AI's balance
        AI_text= Label(window, text="AI balance:", bg='white').pack(side=RIGHT, padx=10, pady=0)
        #button for starting plotting
        b = Button(window, text="Start", command=gui_handler, bg="grey", fg="white")
        b.pack(side=RIGHT, padx=69, pady=0)
        #box where the amount of money either invested or sold is entered
        textBox = Text(window, height=1, width=6)
        textBox.pack(side=RIGHT, padx=25, pady=0)
        #button for buying the stock
        buy_button = Button(window, text="Buy", command=buy,bg="green", fg="white")
        buy_button.pack(side=RIGHT, padx=5, pady=0)
        #button for sellling the stock
        sell_button = Button(window, text="Sell", command=sell, bg="red", fg="white")
        sell_button.pack(side=RIGHT, padx=5, pady=0)
        window.mainloop()

      
      
#Object that belongs to the graph class
Stock_graph = graph()
#Object that belongs to the AI class
Stock_AI=AI()
#runs the app function
Stock_graph.app()

'''Stock from 2016 jan 1 to 2021 september 17 298 weeks'''
'''TSLA, AAPL, GM,, NVDA  '''