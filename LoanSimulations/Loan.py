#Defines the Loan Object for The Simualtions Program
#Written By Hayden Lydick On 6/5/2020
#Contact Info:[Redacted]
#Use at your own risk ya bums

class Loan:
    #Class that defines the loan and its associated values
    def __init__(self, principle = 200000.0, interest_rate = 5.0, loan_length = 10.0):
        self.principle = principle #in dollars
        self.interest_rate = interest_rate/100.0 #in percent
        self.loan_length = loan_length #in years
        self.current_interest = 0.0 #in dollars
        self.TotalBalance = self.principle # intitially balance and principle are identical
        self.accrued_interest = 0.0 #total interest on initial principle
        self.debt_timestep = 0.0 #years since creation
        print('Loan Created...\n' + 'Principle: ' + str(self.principle))
        print('Interest Rate: ' + str(self.interest_rate))
        print('Loan Length (years): ' + str(self.loan_length))

    def CalculateInterest(self, yearly_payments=12, period = 1):
        interest = 0.0 #define as a float for clarity
        interest = self.TotalBalance * (self.interest_rate/yearly_payments)*period #calculate interest for a period
        self.current_interest = self.current_interest + interest #increase the current interest by the new amount
        self.accrued_interest = self.accrued_interest + interest #add to total generated interest on the principle
        self.debt_timestep = self.debt_timestep + period
        return(interest)

    def MakePayment(self, payment = 0.0):
        self.TotalBalance = self.TotalBalance - (payment - self.current_interest)
        if(self.TotalBalance <= 0 ):
            self.TotalBalance = 0
            print('Loan Paid Off...\n\tNo Further Payments Necessary')
        self.current_interest = 0
        print('Payment Made, Total Balance = ', str(round(self.TotalBalance, 2)))
        return(self.TotalBalance)
    
    #function to add current interest to the loan principle
    def Capitalization(self):
        self.TotalBalance = self.TotalBalance + self.current_interest
        self.principle = self.principle + self.current_interest
        self.current_interest = 0 
        self.debt_timestep = 0

    
    
