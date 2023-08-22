import pandas as pd
from connexion import Connexion

connexion = Connexion('BetaPortfolio','root','root')#Connexion('sql7618935','sql7618935','vufErhKP7w')
connexion.initialisation()

def load_transactions(user_id, connexion=connexion): 
    
    #connexion = Connexion('BetaPortfolio','root','root23root23')#Connexion('sql7618935','sql7618935','vufErhKP7w')
    #Fonction qui prend en argument la connexion avec la base de données
    #les transactions sont load dans un dataframe    
    print('before request')
    requete = 'Select distinct * from transactions inner join users on transactions.user_id = users.user_id where username = "{}"'.format(user_id)
    print(requete)
    curseur = connexion.execute(requete)

    df = pd.DataFrame(columns=['Date', 'qty_bought', 'qty_spent', 'fee', 'price', 'fiat', 'crypto',
       'action', 'platform', 'Commentaire'])

    for row in curseur:
        df = pd.concat([df, pd.DataFrame({'Date': [row['date']],
                                      'qty_bought': [row['qty_bought']],
                                      'qty_spent': [row['qty_spent']],
                                      'fee': [row['fee']],
                                      'price': [row['price']],
                                      'fiat': [row['fiat']],
                                      'crypto': [row['crypto']],
                                      'action': [row['action']],
                                      'platform': [row['platform']],
                                      'Commentaire': [row['commentaire']]})])
    return df

def load_users(connexion=connexion):
    #Fonction qui prend en argument la connexion avec la base de données
    #les transactions sont load dans un dataframe    
    requete = 'Select distinct * from users'
    curseur = connexion.execute(requete)

    df = pd.DataFrame(columns=['user_id', 'username', 'password', 'email', 'name', 'vorname'])

    # Dictionary to store the values
    login = {}

    for row in curseur:
        df = pd.concat([df, pd.DataFrame({'user_id': [row['user_id']],
                                      'username': row['username'],
                                      'password' : [row['password']],
                                      'email': [row['email']],
                                      'name': [row['name']],
                                      'vorname': [row['vorname']],
                                      })])
        
        #login[row['email']] = row['password']
        login[row['username']] = row['password']
        
    return df, login
    
#users_data = load_users(connexion)
#load_users_login = users_data[1]
#load_users_info = users_data[0]

#connexion.close_connexion()

#if __name__ == "__main__":

    #print(load_users_login)
    #df = user_login('user1@example.com','password1',connexion)[0]
    #print(1)#df)
    #print(username)
    
    #connexion.close_connexion()