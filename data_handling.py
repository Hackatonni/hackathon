import pandas as pd

#==============================================================================
# questo file contiene le funzioni per il caricamento e la gestione dei dati
# questo file sarà il ponte tra il dataset e il modello di machine learning
# le funzioni in questo file saranno utilizzate per caricare i dati, preprocessarli e prepararli per il modello
# specularmente, il file si occuperà di salvare i risultati del modello e prepararli per l'invio al frontend
#==============================================================================


# Funzione per caricare i dati dal file CSV e preparare i DataFrame necessari
# inoltre la funzione filtra i dati in base agli ID disponibili nel dataset di embedding
# ritorna un dizionario con i DataFrame e gli ID del dataset
def load_data(ds_file_path, embeddings_file_path):
    # load the dataset from a CSV file
    print('Loading dataset...')
    df_complete = pd.read_csv(ds_file_path, nrows=500000, low_memory=False)
    
    df_emb = pd.read_csv(embeddings_file_path, low_memory=False)
    # Assicurati che la colonna 'id' sia presente in entrambi i DataFrame e sia dello stesso tipo
    df_complete['id'] = df_complete['id'].astype(str)
    df_emb['id'] = df_emb['id'].astype(str)
    
    # genero un df più piccolo a partire dal df_complete
    df_ids_cats = df_complete[['id', 'categories']]
    
    # Unisci solo le colonne necessarie da df_dataset
    df_emb = df_emb.merge(df_ids_cats[['id', 'categories']], on='id', how='left')

     # filtro il dataset in base agli ID disponibili nel dataset di embedding
    df_ids_cats = df_ids_cats[df_ids_cats['id'].isin(df_emb['id'])]
    
    # filtro il dataset in base agli ID disponibili nel dataset di embedding
    df_emb = df_emb[df_emb['id'].isin(df_ids_cats['id'])]
    
    print('Dataset loaded successfully.')
    
    #ritorno un dizionario con i DataFrame e gli ID del dataset 
    return {'df_emb': df_emb, 'df_complete': df_complete, 'dataset_ids': df_ids_cats}