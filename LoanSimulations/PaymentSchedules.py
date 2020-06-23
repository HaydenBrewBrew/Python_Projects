from abc import ABC, abstractmethod
from Loan import Loan


#abstract class to define all types of payment schedules
class PaymentSchedule(ABC):

    #Abstract method for all repayment plans to implement
    def SetMonthlyPayment(self, loan):
        pass
    
    def __init__(self, payment_frequency = 12):
        self.payment_frequency = payment_frequency# payments per year
        self.debt_timestep = 0
        self.payment = 0
    
    #checks current payment against the timestep and the rule established 
    def CurrentPayment(self, loan):
        pass

#object that defines the standard repayment schedule for a given loan amount 
class Standard_Repayment(PaymentSchedule):

    #set monthly payments as an amotorized payment of interest and principle
    def SetMonthlyPayment(self, loan):
        self.payment = 0.0
        payments = self.payment_frequency * loan.loan_length
        a_rate = float(loan.interest_rate)/float(self.payment_frequency)
        #payment amotorized loan rate
        p =  loan.principle*(a_rate*(1 + a_rate)**(payments))/((1+a_rate)**payments - 1)
        self.payment = round(p,2)
        print('Standard Repayment Payment:' + str(self.payment))
    
    #construct object and set the monthly payment amount
    def __init__(self, loan, payment_frequency = 12):
        super(Standard_Repayment, self).__init__(payment_frequency)
        self.SetMonthlyPayment(loan)

    #obtain current payment and update current payment 
    def CurrentPayment(self, loan):
        self.SetMonthlyPayment(loan)
        payment = self.payment*(loan.debt_timestep - self.debt_timestep)
        self.debt_timestep = loan.debt_timestep
        return(payment)

#object that defines the Extended repayment schedule for a given loan amount 
class Extended_Repayment(PaymentSchedule):

    #updates the current payment based off a given loan
    def SetMonthlyPayment(self, loan):
        self.payment = 0.0
        payments = self.payment_frequency * loan.loan_length
        a_rate = float(loan.interest_rate)/float(self.payment_frequency)
        p =  loan.principle*(a_rate*(1 + a_rate)**(payments))/((1+a_rate)**payments - 1)
        self.payment = round(p,2)
        print('Extended Repayment Payment: ' + str(self.payment))

    #constructor
    def __init__(self, loan, payment_frequency = 12.0, adjusted_length = 25.0):
        super(Extended_Repayment, self).__init__(payment_frequency)

        #adjust loan length for a longer period of time
        if adjusted_length > loan.loan_length:
            loan.loan_length = adjusted_length
            print('New Loan Length: ' + str(loan.loan_length))
        else:
            print('Warning: New Loan Length Shorter than Original Length...\n')

        self.SetMonthlyPayment(loan)

    #obtain current payment and update current payment
    def CurrentPayment(self, loan):
        self.SetMonthlyPayment(loan)
        payment = self.payment*(loan.debt_timestep - self.debt_timestep)
        self.debt_timestep = loan.debt_timestep
        return(payment)

#object that defines the repayment schedule for a graduate repayment loan
#Assumes that the graduated repayment period is paying off interest only, then swaps to paying the principle for the remaining loan period   
class Graduated_Repayment(PaymentSchedule):
    
    #checks to confirm if you are out of the graduated repayment period
    #adjusts the loan amount accordingly, and assume that grad repayment is interest only payments
    def SetMonthlyPayment(self, loan):
        self.payment = 0
        c_years  = float(self.debt_timestep)/float(self.payment_frequency)
        a_rate = float(loan.interest_rate)/float(self.payment_frequency) #ajusted rate per payment period
        if c_years < self.graduated_period:
            self.payment = round((loan.principle * a_rate),2)
        else:
            adj_length = (loan.loan_length - self.graduated_period) #adjust effective length of the loan by the graduate repayment period
            payments = adj_length*self.payment_frequency #new total payment count
            p = loan.principle*(a_rate*(1 + a_rate)**(payments))/((1+a_rate)**payments - 1)
            self.payment = round(p,2)
        print('Graduate Repayment Payment:' + str(self.payment))


    #adjust loan length for a longer period of time
    def __init__(self, loan, payment_frequency = 12,graduated_period=2.0):
        super(Graduated_Repayment, self).__init__(payment_frequency) 
        self.graduated_period = graduated_period
        self.SetMonthlyPayment(loan)

    #obtain current payment and update current payment
    def CurrentPayment(self, loan):
        self.SetMonthlyPayment(loan)
        payment = self.payment*(loan.debt_timestep - self.debt_timestep)
        self.debt_timestep = loan.debt_timestep
        return(payment)


class ICR(PaymentSchedule):

    def SetMonthlyPayment(self,loan):
        self.payment = 0
        #calculate the threshold payment to be made 
        last_income = len(self.income_history) - 1
        d_max_payment = self.payment_thresh * self.CalcDiscretionaryIncomeMonthly(self.poverty_line,self.income_history[last_income][0]) #sets max payment
        self.payment = d_max_payment
        print('ICR Payment: ' + str(self.payment))

    #expand this function at some point
    def CalcDiscretionaryIncomeMonthly(self, poverty_line, income):
        dis_income = float(0.75*float(income) - 1.5*poverty_line)/12.0 #assume 1/4 in taxes
        if dis_income < 0:
            print('Warning: No Income Reported...\n\tRestart simulation if unintentional...')
            return 0.0
        else:
            return(dis_income)
    
    def __init__(self, loan, payment_frequency = 12 , income=60000, poverty_line = 12000.00, payment_thresh=0.2, adjusted_length = 25.0):
        super(ICR,self).__init__(payment_frequency)
        #adjust loan length for a longer period of time
        if adjusted_length > loan.loan_length:
            loan.loan_length = adjusted_length
            print('New Loan Length: ' + str(loan.loan_length))
        else:
            print('Warning: New Loan Length Shorter than Original Length...\n')
        #initialize the storage of the income data
        self.debt_timestep = 0
        self.income_history = []
        self.income_history.append([])
        self.income_history.append([])
        #to set the current income timesteps
        self.income_history[0].append(0) #income
        self.income_history[0].append(0) #Starting timepoint
        self.income_history[0].append(0) #ending timepoint

        self.income_history[1].append(income)   #set current income
        self.income_history[1].append(self.debt_timestep) #set the timepoint of the object when this income was earned
        self.income_history[1].append(0)

        self.payment_thresh = payment_thresh
        self.poverty_line = poverty_line
        self.SetMonthlyPayment(loan)

    def CurrentPayment(self, loan):
        self.SetMonthlyPayment(loan)
        payment = self.payment*(loan.debt_timestep - self.debt_timestep)
        self.debt_timestep = loan.debt_timestep
        return(payment)

    def ChangeIncomeLevel(self, new_income):
        last_income = len(self.income_history) - 1 #zero indexing
        self.income_history[last_income][2] = (self.debt_timestep - 1)#set to -1 for now by assuming the all timesteps are integers
        #add in new income history
        self.income_history.append([])
        self.income_history[last_income + 1].append(new_income)
        self.income_history[last_income +  1].append(self.debt_timestep)
        self.income_history[last_income +  1].append(0)
        #no need to call SetMonthlyPayment, it is called during every payment iteration anyway

#same idea as ICR but Standard amotorized is the theoretical maximum
class IBR(PaymentSchedule):

    def __init__(self, loan, payment_frequency = 12 , income=60000, poverty_line = 12000.00, payment_thresh=0.15, adjusted_length = 25.0):
        super(IBR,self).__init__(payment_frequency)
        self.payment_frequency = payment_frequency
        #adjust loan length for a longer period of time
        if adjusted_length > loan.loan_length:
            loan.loan_length = adjusted_length
            print('New Loan Length: ' + str(loan.loan_length))
        else:
            print('Warning: New Loan Length Shorter than Original Length...\n')
        #initialize the storage of the income data
        self.debt_timestep = 0
        self.income_history = []
        self.income_history.append([])
        self.income_history.append([])
        #to set the current income timesteps
        self.income_history[0].append(0) #income
        self.income_history[0].append(0) #Starting timepoint
        self.income_history[0].append(0) #ending timepoint

        self.income_history[1].append(income)   #set current income
        self.income_history[1].append(self.debt_timestep) #set the timepoint of the object when this income was earned
        self.income_history[1].append(0)

        self.payment_thresh = payment_thresh
        self.poverty_line = poverty_line
        self.SetMonthlyPayment(loan)
    
    def ChangeIncomeLevel(self, new_income):
        last_income = len(self.income_history) - 1 #zero indexing
        self.income_history[last_income][2] = (self.debt_timestep - 1)#set to -1 for now by assuming the all timesteps are integers
        #add in new income history
        self.income_history.append([])
        self.income_history[last_income + 1].append(new_income)
        self.income_history[last_income +  1].append(self.debt_timestep)
        self.income_history[last_income +  1].append(0)
        #no need to call SetMonthlyPayment, it is called during every payment iteration anyway

    def CurrentPayment(self, loan):
        self.SetMonthlyPayment(loan)
        payment = self.payment*(loan.debt_timestep - self.debt_timestep)
        self.debt_timestep = loan.debt_timestep
        return(payment)
    
    def SetMonthlyPayment(self,loan):
        self.payment = 0
        #calculate the threshold payment to be made 
        last_income = len(self.income_history) - 1
        d_max_payment = self.payment_thresh * self.CalcDiscretionaryIncomeMonthly(self.poverty_line,self.income_history[last_income][0]) #sets max payment
        a_rate = loan.interest_rate/12
        payments = self.payment_frequency * 10 #10 year rate is the max payment
        a_max_payment = loan.principle*(a_rate*(1 + a_rate)**(payments))/((1+a_rate)**payments - 1)
        if a_max_payment < d_max_payment:
            self.payment = a_max_payment
        else:
            self.payment = d_max_payment
        print('ICR Payment: ' + str(self.payment))

    #expand this function at some point
    def CalcDiscretionaryIncomeMonthly(self, poverty_line, income):
        dis_income = float(0.75*float(income) - 1.5*poverty_line)/12.0 #assume 1/4 in taxes
        if dis_income < 0:
            print('Warning: No Income Reported...\n\tRestart simulation if unintentional...')
            return 0.0
        else:
            return(dis_income)
        




#class PAYE(PaymentSchedule):


#class REPAYE(PaymentSchedule):
