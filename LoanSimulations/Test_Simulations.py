from Loan import Loan
from PaymentSchedules import Standard_Repayment
from PaymentSchedules import Extended_Repayment
from PaymentSchedules import Graduated_Repayment
from PaymentSchedules import ICR
l = Loan()
p = ICR(l, income = 60000)
total_payment_count = l.loan_length*p.payment_frequency
stepsize = 1
medschool = 12 * 4 #months of forebearance
l.CalculateInterest(period = 12*4)
l.Capitalization()
#residency starts
p.ChangeIncomeLevel(60000)
while l.debt_timestep < total_payment_count:
    if l.debt_timestep == 12.0 * 6:
        p.ChangeIncomeLevel(200000)
    l.CalculateInterest(period=stepsize)
    payment = p.CurrentPayment(l)
    l.MakePayment(payment=payment)
