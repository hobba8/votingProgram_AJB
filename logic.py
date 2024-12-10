from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow,Ui_VotingProgram):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.voter_list = []    #a list to add every successful vote to
        self.jane_votes = 0     #used to track the total count of votes for Jane
        self.john_votes = 0     #used to track the total count of votes for Jane
        self.button_submit_vote.clicked.connect(lambda : self.cast_vote())

        with open('Voter Record.csv', 'w', newline='') as new_file:
            '''
            This initializes the voter list
            with a header.
            '''
            writer = csv.writer(new_file)
            temp = ["Voter ID", "Candidate"]
            writer.writerow(temp)

    def cast_vote(self):
        '''
        This definition functions once you hit the cast vote button.
        It gets the voter id text and candidate, checks the voter id,
        and records the voter id and the vote in a file if the voter id
        is good and unique.
        :return: none
        '''

        voter_id_txt = self.input_voter_id.text().strip()
        voter_id_num, correct = self.check_voter_id(voter_id_txt)

        if correct == 'y':
            if voter_id_num not in self.voter_list:  #checks to ensure the voter id is original
                if self.radio_Jane.isChecked():
                    self.jane_votes +=1
                    self.voter_list.append(voter_id_num)
                    self.input_voter_id.clear()
                    self.input_voter_id.setFocus()
                    if self.button_group1.checkedButton() != 0:  #this resets the buttons
                        self.button_group1.setExclusive(False)
                        self.button_group1.checkedButton().setChecked(False)
                        self.button_group1.setExclusive(True)
                    self.label_vote_status.setStyleSheet("color: green;")  #updates text to indicate successful vote
                    self.label_vote_status.setText("Thank you for voting!") #updates text to indicate successful vote
                    print(f'John - {self.john_votes} votes, Jane - {self.jane_votes} votes - Total Votes = {self.john_votes + self.jane_votes} votes')
                    self.record_vote(voter_id_num,'Jane') #passes the successful vote to the module that records it to a file
                elif self.radio_john.isChecked():
                    self.john_votes += 1
                    self.voter_list.append(voter_id_num)
                    self.input_voter_id.clear()
                    self.input_voter_id.setFocus()
                    if self.button_group1.checkedButton() != 0:
                        self.button_group1.setExclusive(False)
                        self.button_group1.checkedButton().setChecked(False)
                        self.button_group1.setExclusive(True)
                    self.label_vote_status.setStyleSheet("color: green;")
                    self.label_vote_status.setText("Thank you for voting!")
                    print(f'John - {self.john_votes} votes, Jane - {self.jane_votes} votes - Total Votes = {self.john_votes + self.jane_votes} votes')
                    self.record_vote(voter_id_num, 'John')
            else:
                '''
                This code executes if the voter id was already recorded.
                '''
                self.label_vote_status.setStyleSheet("color: red;")
                self.label_vote_status.setText("You Already Voted")
                self.input_voter_id.clear()
                self.input_voter_id.setFocus()
                if self.button_group1.checkedButton() != 0:
                    self.button_group1.setExclusive(False)
                    self.button_group1.checkedButton().setChecked(False)
                    self.button_group1.setExclusive(True)

    def check_voter_id(self, voter_id_txt):
        '''
        This definition evaluates the text the user entered for a voter id,
        determines if it can be converted to an integer and returns the voter id
        if that checks out.
        :param voter_id_txt: this is the text the user enters for their voter id
        :return: the voter id as an int or a negative number if the id is bad
        '''
        try:
            id_num = int(voter_id_txt)
            if id_num >= 0:
                return id_num, 'y'  #returns the voter id if the id can be a positive integer
            else:
                '''
                executes if the number is less than zero.
                '''
                self.label_vote_status.setText("Enter a correct voter id")
                self.label_vote_status.setStyleSheet("color: red;")
                self.input_voter_id.clear()
                self.input_voter_id.setFocus()
                return -1, 'n'
        except ValueError:
            '''
            Executes if the entry create a valueError
            '''
            self.label_vote_status.setStyleSheet("color: red;")
            self.label_vote_status.setText('Enter a correct voter id')
            self.input_voter_id.clear()
            self.input_voter_id.setFocus()
            return -1,'n'

    def record_vote(self, id_number, name):
        '''
        This definition records a successful vote into a csv file.
        :param id_number: the voter id number
        :param name: this is the candidate's name that was selected
        :return: none
        '''
        with open('Voter Record.csv', 'a', newline = '') as new_file:
            writer = csv.writer(new_file)
            temp = [id_number,name]
            writer.writerow(temp)

