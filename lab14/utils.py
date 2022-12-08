'''
Through simulation evaluate the extinction probability within  generation  i  (q_i) and the asymptotic extinction  probability  
(q) for  a Galton-Watson process in which the number of children of an individual Y is  distributed 
as a Poisson(lambda) R.V.  with lambda=0.6, 0.8, 0.9 0.95, 0.99, 1.01, 1.05, 1.1, 1.3.

Compare the results you  obtain with theoretical predictions, (by  finding numerically, when needed,  
the solution of q= phi_Y(q)) 

In particular, you are requested to specify the stopping condition you have implemented in order to empirically 
"detect"   non-extinction condition.  Please try to provide a theoretical justification to such condition.

For the case  \lambda=0.8, obtain the empirical distribution (histogram) on the number of nodes in the tree.
'''


# vogliamo arrivare alla extinsion probability (q_i) per ogni i
# comprese quelle asintotiche
# dove il numero di Y è distribuito come una poisson(lambda) (ricontrolla il laboratorio sulla generazione delle r.v.)
# per capire come si genera

# INPUT SIMULATION PARAMETER
tree_depth = 1000 # first stopping condition
# second stopping condition: when the generation is empty
# potentialmente possiamo pensare di creare una lista prima del ciclo while con il root dentro inizialmente
# ed ogni volta che una generazione viene creata, i children diventano automaticamente parent
# e quindi root dai quali si generano altri children
# potrebbere essere utile aumentare un counter ad ogni ciclo while tale per cui quando ranggiunge counter == tree_max_depth
# allor si stoppa il processo
# pensa al fatto che il parametro della poisson potrebbe essere il nostro reproducing factor

