from experta import *
from termcolor import colored


class Loan(Fact):
    pass

class Reasons:
    reasons = ['family','accidents','hospital']

class LoanMessages:
    accept = colored("Congrats You are eligible for Loan\n", 'green')
    decline = colored("Sorry Your Loan Can't be approved\n",'red')
    speakwithManager = colored("You might be eliglible for a loan, You can reach out to our manager for more inforomation\n","yellow")

class LoanApplication(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Loan(action="precheck")
        yield Loan(name=(input("Whats Your Name?")))

    @Rule(Loan(action='precheck'),
          NOT(Loan(cS=W())))
    def get_credit_info(self):
        #self.declare(Loan(name=input("What's Your Name? ")))
        self.declare(Loan(cS=int(input("Credit Score ?"))))


    #rule if minimum credit score doesn't meet
    @Rule(Loan(action='precheck'),Loan(cS=P(lambda cS: cS < 450) | P(lambda cS: cS > 650)))
    def credit_Validation(self):
        print(LoanMessages.decline)

    #rule after meeting credit score
    @Rule(Loan(action='precheck'),Loan(cS=P(lambda cS: cS >= 450) & P(lambda cS: cS <= 650)))
    def credit_next(self):
        self.declare(Loan(recurringMonthlyDebit=int(input("What is your Monthly Recurring Monthly Debit? "))))
        self.declare(Loan(grossMonthlyIncome=int(input("What is your Gross Recurring Monthly income? "))))

    #rule if gross Monthly Income doesn't meet
    @Rule(Loan(action='precheck'),Loan(grossMonthlyIncome=P(lambda grossMonthlyIncome: grossMonthlyIncome < 1500)))
    def gross_Monthly_Validation(self):
        print(colored("\nSorry Your Gross Montthly Income is Less than 1500 doesn't qualify for Loan\n","yellow"))
        print(LoanMessages.speakwithManager)
    
    #rule if gross Monthly Income Meets
    @Rule(Loan(action='precheck'),
    Loan(grossMonthlyIncome=P(lambda grossMonthlyIncome: grossMonthlyIncome > 1500)),
    (AS.ds << Loan(grossMonthlyIncome=MATCH.grossMonthlyIncome)),
    (AS.fv << Loan(recurringMonthlyDebit=MATCH.recurringMonthlyDebit)))
    def gross_Monthly_next(self,ds,fv,grossMonthlyIncome,recurringMonthlyDebit):
        debitRatioIncome = recurringMonthlyDebit/grossMonthlyIncome
        if debitRatioIncome*100 > 15:
            #decline if debit to income ratio is higer than 15
            print(LoanMessages.speakwithManager)
        else:
            self.declare(Loan(preChecks='done'))
    
    #rule after running pre checks
    @Rule(Loan(action='precheck'),Loan(preChecks='done'))
    def start_application(self):
        self.declare(Loan(bankR=input("Do you have any bankrupties in past? Yes or No\n").lower()))
        self.declare(Loan(LatePayments=input("Do you have any Late Payments?\n")))
            

    #rule to invoke if there are Late Payments
    @Rule(Loan(action='precheck'),Loan(preChecks='done'),Loan(LatePayments='yes'))
    def latePayments(self):
        latepayDays = int(input("Choose \n1)30-60 Days\n2)60-90 Days\n3) 90-120 Days"))
        howmanytimes = int(input("How Many Late Payments? \n"))
        if latepayDays in [1,2,3]:
            self.declare(Loan(latepayDays=latepayDays))
            self.declare(Loan(howmanytimes=howmanytimes))
        else:
            print("Choose Correction Option")

    #rule to invoke if there are Late Payments less than 4 and latepay days 30-60
    @Rule(AND(Loan(action='precheck'),Loan(preChecks='done'),
    Loan(latepayDays=1),
    Loan(howmanytimes=P(lambda howmanytimes: howmanytimes < 5))
    ))
    def latepayment_less_than_4(self):
        reason = input("What's the reason for latepayments?\nfamily\naccidents\nhealth\n").lower()
        if reason in Reasons.reasons:
            print(LoanMessages.accept)


    #rule to invoke if there are Late Payments more than 5 and latepay days 30-60
    @Rule(AND(Loan(action='precheck'),Loan(preChecks='done'),
    Loan(latepayDays=1),
    Loan(howmanytimes=P(lambda howmanytimes: howmanytimes > 5))
    ))
    def latepayment_greater_than_5(self):
        print(LoanMessages.decline)

    #rule to invoke if there are Late Payments less than 4 and latepay days 60-90
    @Rule(AND(Loan(action='precheck'),Loan(preChecks='done'),
    Loan(latepayDays=2),
    Loan(howmanytimes=P(lambda howmanytimes: howmanytimes < 2))
    ))
    def latepayment_less_than_2(self):
        reason = input("What's the reason for latepayments?\nfamily\naccidents\nhealth\n").lower()
        if reason in Reasons.reasons:
            print(LoanMessages.accept)


    #rule to invoke if there are Late Payments more than 5 and latepay days 60-90
    @Rule(AND(Loan(action='precheck'),Loan(preChecks='done'),
    Loan(latepayDays=2),
    Loan(howmanytimes=P(lambda howmanytimes: howmanytimes > 2))
    ))
    def latepayment_greater_than_2(self):
        print(LoanMessages.decline)
    
    #rule to invoke if there are Late Payments less than 4 and latepay days 90-120
    @Rule(AND(Loan(action='precheck'),Loan(preChecks='done'),
    Loan(latepayDays=3)
    ))
    def latepayDays_g_90(self):
        print(LoanMessages.decline)





engine = LoanApplication()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!