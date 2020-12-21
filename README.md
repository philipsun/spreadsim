# DynSimWorld

This is a simple implementation for simulating a dyanmic wolrd where some virus can be spreaded as people are moving and contacting.

I use pygame+agent model+monte carlo method to simulate people's states: including moving, contacting, health status and medication treatments they are in.

You need to run it in pygame enviroment.

The core modelling is done in class sxpNCPState.InfectPersion

YOu may setup your own model for the function infectother()

where, you can define how people are affected by some probability model.

For example, in this simple case, I use：
    
    region = self.probsel({'pub':1-pstayhome,'home':pstayhome})

to controll how people will stay at home or go to pub.

If stay home, the infection will be limited to the family range, otherwise, the infection will be spread open to public people, where higher probability of infecting others can be defined.

In this simple model, you will say a vibrating curvs of number of infected peoples due to the probability model is being in inverse relationship to the risk probability they can sense.

This will lead to a negative feedback to the whole system's runninging and finally will lead to a up and down developing of virus spreading.

There are also many places where you can model, for example, how a people's health will develop. How if they cannot get enough care and so on.