import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import random
import numpy as np
from utilities import user_interest_filtering, random_not_user_interests, macro_categories, sub_categories
from data_handling import load_data

#df = load_data('/Users/enricotazzer/Desktop/hackathon/data/arxiv_dataset.csv', '/Users/enricotazzer/Desktop/hackathon/data/arxiv_specter_embeddings.csv') # Replace with actual file paths
    
def extract_samples(macro_categories=None, sub_categories=None,nsamples=50, p_subcat=60, p_randcat=40):
    """
    extract_samples è il metodo che fornisce gli articoli da valutare durante la fase
    di registrazione.
    - sub_categories è la lista dei codici delle sottocategorie preferite dall'utente
    - macro_categories è la lista dei codici delle categorie preferite dall'utente
    - p_subcat è la percentuale di articoli da selezionare e presi dalle sottocategorie
    - p_randcat è la percentuale di articoli da selezionare e presi random dalle macro categorie
    - nsamples è il numero di articoli che verranno ritornati
    Il metodo restituisce una lista di nsamples articoli così composta:
    - p_subcat% di articoli presi dalle sottocategorie
    - p_randcat% di articoli presi dalle macro categorie
    - il resto degli articoli è preso random dal dataset

    Il metodo restituisce un DataFrame con tutte le informazioni degli articoli selezionati contenute nel dataset df 
    df_ids_cat è un DataFrame che contiene gli ID degli articoli e la lista delle categorie associate a ciascun articolo
    df è il DataFrame che contiene tutte le informazioni degli articoli, tra cui l'ID, il titolo, le categorie, l'abstract e le informazioni di pubblicazione.
    """
    global df, df_ids_cats

    print("Inizio estrazione campioni...")
    print("Macro categorie selezionate:", macro_categories)
    print("Sottocategorie selezionate:", sub_categories)


    # estraggo gli indici degli articoli appartenenti a una sottocategoria
    if sub_categories:
        mask_sub = df_ids_cats['categories'].apply(
            lambda x: isinstance(x, str) and any(cat in x.split() for cat in sub_categories)
        )
        df_sub = df_ids_cats[mask_sub]
    else:
        print("cazzo")
        #df_sub = pd.DataFrame(columns=df_ids_cats.columns)
    # estraggo gli indici degli articoli appartenenti a una macro categoria
    if macro_categories:
        mask_macro = df_ids_cats['categories'].apply(
            lambda x: isinstance(x, str) and any(cat in x.split() for cat in macro_categories)
        )
        df_macro = df_ids_cats[mask_macro]


    print("DF_MACRO: ", df_macro)
    # calcolo il numero di articoli da selezionare dalle sottocategorie e dalle macro categorie
    n_sub = int(nsamples * p_subcat / 100)
    n_rand = int(nsamples * p_randcat / 100)
    # seleziono gli articoli dalle sottocategorie
    if not df_sub.empty:
        df_sub_sample = df_sub.sample(n=min(n_sub, len(df_sub)), random_state=42)
    else:
        print("cazzo cazzo cazzo cazzo")
        #df_sub_sample = pd.DataFrame(columns=df_ids_cats.columns)
    
    # seleziono gli articoli dalle macro categorie
    if not df_macro.empty:
        df_macro_sample = df_macro.sample(n=min(n_rand, len(df_macro)), random_state=42)
    else:
        print("cazzo cazzo cazzo cazzo cazzo")
        #df_macro_sample = pd.DataFrame(columns=df_ids_cats.columns)
    
    
    # unisco i due DataFrame
    df_samples = pd.concat([df_sub_sample, df_macro_sample], ignore_index=True)
    # se il numero di articoli selezionati è inferiore a nsamples, aggiungo articoli random presi dalle macro categorie
    if df_ids_cats is None or df_ids_cats.empty:
        raise ValueError("df_ids_cats non può essere vuoto. Assicurati di aver caricato il dataset correttamente.")
    if len(df_samples) < nsamples:
        # calcolo il numero di articoli da aggiungere
        n_add = nsamples - len(df_samples)
        # seleziono articoli random dalle macro categorie
        df_rand_sample = df_ids_cats.sample(n=n_add, random_state=42)
        # unisco i due DataFrame
        df_samples = pd.concat([df_samples, df_rand_sample], ignore_index=True)
    
    # se il numero di articoli selezionati è superiore a nsamples, riduco il numero di articoli
    if len(df_samples) > nsamples:
        df_samples = df_samples.sample(n=nsamples, random_state=42)
    # unisco i campi del DataFrame df con quelli di df_ids_cats
    df_samples = df.merge(df_samples, on='id', how='inner')
    # seleziono le colonne che mi interessano
    #df_samples = df_samples[['id', 'title', 'categories', 'abstract', 'authors', 'published']]
    # resetto l'indice
    df_samples.reset_index(drop=True, inplace=True)
    # ritorno il DataFrame con gli articoli selezionati
    return df_samples

"""
def knn_recommender(user_interests):
    if not isinstance(user_interests, list): ## concorrenza attendere file registration.json
        raise ValueError("user_interests must be a list of categories.")
    
    df_user = user_interest_filtering(user_interests)
    embedding_cols = [col for col in df_user.columns if col not in ['id', 'categories', 'title']]
    embeddings = df_user[embedding_cols].values
    y = df_user.index
    nn = KNeighborsClassifier(n_neighbors=100, metric='cosine', n_jobs=-1)
    nn.fit(embeddings, y)
    idxs = [np.random.randint(0, len(y)-1) for _ in range(10)]  # Randomly select 10 indices from the user dataset
    mean_embedding = np.mean(embeddings[idxs, :], axis=0)
    dist, index = nn.kneighbors(X=mean_embedding.reshape(1, -1))
    best_reccomendation = index[:70][0]
    worst_reccomendation = index[-10:][0]
    random_recommendation = random_not_user_interests(df, user_interests)
    recommendations = pd.concat([df_user.iloc[best_reccomendation], df_user.iloc[worst_reccomendation], random_recommendation])
    return recommendations.loc[:, ['id', 'title']]

"""

def code2description(code):
    # Macro category
    if code in macro_categories:
        return macro_categories[code]
    # Subcategory
    for macro, subs in sub_categories.items():
        for sub_code, desc in subs:
            if code == sub_code:
                return desc
            
def raw2codes(raw_topics=None, raw_subtopics=None):
    # estraggo la lista di codici che sono contenute nella macro categoria
    # i codici sono nella forma "macro.sub"
    if raw_topics is None or raw_subtopics is None:
        raise ValueError("raw_topics e raw_subtopics devono essere specificati.")
    topics_codes = []
    # estraggo i codici delle macro categorie
    for topic in raw_topics:
        found = False
        for macro, desc in macro_categories.items():
            if topic == desc or topic == macro:
                topics_codes.append(macro)
                found = True
                break
        if not found:
            raise ValueError(f"{topic} non è una macro categoria valida.")
    print(f"Macro categories: {topics_codes}")
    
    # per ogni macro categoria contenuta in topics_codes, estraggo la lista delle sottocategorie
    macro_areas_codes = []
    for macro in topics_codes:
        if macro not in sub_categories:
            raise ValueError(f"{macro} non ha sotto categorie valide.")
        macro_areas_codes.extend([code for code, desc in sub_categories[macro]])
    print(f"Sub categories: {macro_areas_codes}")

    # estraggo da sub_categories i codici che hanno come prefisso una macro categoria contenuta in topics_codes
    subtopics_codes = []
    for subtopic in raw_subtopics:
        found = False
        for macro in topics_codes:
            for code, desc in sub_categories.get(macro, []):
                if subtopic == desc or subtopic == code:
                    subtopics_codes.append(code)
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f"{subtopic} non è una sotto categoria valida.")
    
    return topics_codes, macro_areas_codes, subtopics_codes


from sklearn.metrics.pairwise import cosine_similarity


"""
naive recommender: restituisce i documenti più simili all'embedding medio degli articoli che l'utente ha valutato
senza aggiornamento rispetto al dominio di interesse dell'utente.
la versione futura dovrebbe prevedere 
- l'aggiornamento sulla base delle nuove categorie piaciute
- una nuova metodologia di esploration-exploitation
"""
def recommendation_weighted(user_feedback):
    global df_ids_cats, df_emb, df
    """
    user_feedback = [
        # Esempio:
        # {'id': '2505.10224', 'embedding': np.array([...]), 'like': 1, 'clicks': 3},
        # {'id': '2505.10225', 'embedding': np.array([...]), 'like': -1, 'clicks': 1},
        # ...
    ]
    """

    # Costruisci array di embeddings e pesi
    embeddings_list = []
    weights = []
    for item in user_feedback:
        emb = item['embedding']
        # Salta se l'embedding non è valido
        if emb is None or not hasattr(emb, "shape"):
            continue
        # Flatten se necessario
        if len(emb.shape) == 2 and emb.shape[0] == 1:
            emb = emb.flatten()
        embeddings_list.append(emb)
        # Peso: like/dislike ha molto peso, i click aumentano il peso
        like = item['like'][0] if isinstance(item['like'], list) else item['like']
        try:
            like_weight = 10 * int(like)  # like=1 -> +10, dislike=-1 -> -10, 0 -> 0
        except Exception:
            like_weight = 0
        click_weight = int(item['clicks'][0]) if isinstance(item['clicks'], list) else int(item['clicks'])
        total_weight = like_weight + click_weight
        weights.append(total_weight)
    
    if not embeddings_list or not weights:
        print("Nessun embedding valido trovato in user_feedback.")
        return [], []

    embeddings_arr = np.vstack(embeddings_list)
    weights_arr = np.array(weights)

    # Assicura che weights_arr abbia la stessa lunghezza di embeddings_arr lungo axis=0
    if embeddings_arr.shape[0] != weights_arr.shape[0]:
        print("Mismatch tra numero di embeddings e pesi, controllo dati.")
        return [], []

    # Normalizza i pesi (opzionale, solo se vuoi che la somma sia 1)
    if np.sum(np.abs(weights_arr)) > 0:
        weights_arr = weights_arr / np.sum(np.abs(weights_arr))

    # Calcola l'embedding pesato del gruppo
    group_embedding_weighted = np.average(embeddings_arr, axis=0, weights=weights_arr).reshape(1, -1)

    # Prendi solo le colonne embedding da df_emb (solo float, escludi tutte le colonne non numeriche)
    exclude_cols = ['id', 'categories', 'title', 'abstract', 'authors', 'published']
    embedding_cols = [col for col in df_emb.columns if col not in exclude_cols and np.issubdtype(df_emb[col].dtype, np.number)]
    all_embeddings = df_emb[embedding_cols].values

    # uso kNN per trovare i documenti più simili
    from sklearn.neighbors import NearestNeighbors
    nn = NearestNeighbors(n_neighbors=100, metric='cosine', n_jobs=-1)
    nn.fit(all_embeddings)
    distances, indices = nn.kneighbors(group_embedding_weighted)
    similar_indices = indices[0]
    # Prendi i documenti validi
    similar_docs = df_emb.iloc[similar_indices].copy()
    # Calcola la similarità coseno tra l'embedding del gruppo e gli embeddings dei documenti simili
    similarities = cosine_similarity(group_embedding_weighted, similar_docs[embedding_cols].values).flatten()
    # Aggiungi le similarità come colonna al DataFrame dei documenti simili
    similar_docs['similarity'] = similarities
    # Ordina i documenti simili per similarità in ordine decrescente
    similar_docs = similar_docs.sort_values(by='similarity', ascending=False)
    # Prendi i primi 50 documenti come raccomandazioni
    recommendations = similar_docs.head(50)
    # Aggiungi le categorie e i titoli al DataFrame delle raccomandazioni
    recommendations = recommendations.merge(df_ids_cats[['id', 'categories']], on='id', how='left')
    recommendations = recommendations.merge(df[['id', 'title']], on='id', how='left')
    # Ritorna le raccomandazioni come lista di dizionari
    recommendations_list = recommendations.to_dict(orient='records')
    #for rec in recommendations_list:
    #    rec['categories'] = rec['categories'].split() if isinstance(rec['categories'], str) else []
    #    rec['title'] = rec.get('title', 'No title available')
    return recommendations_list, similar_docs




def actions_parsed(user_actions):
    global df, df_emb, df_ids_cats
    embedding_cols = [col for col in df_emb.columns if col not in ['id', 'categories', 'title']]
    data = []
    for action in user_actions:
        actions = user_actions[action]
        dic = {}
        dic["id"] = action
        dic["clicks"] = actions["clicks"]
        dic["like"] = actions["likes"]
        dic["time_spent"] = actions["time_spent"]
        dic["embedding"] = df_emb[df_emb["id"] == action][embedding_cols].values[0] if not df_emb[df_emb["id"] == action].empty else None
        data.append(dic)
    return data



def wait_user_interests():
    # check if there exist user_registration_info.json
    while not os.path.exists('user_registration_info.json'):
        pass
    with open('user_registration_info.json', 'r') as f:
        user_registration_info = json.load(f)
        raw_topics = user_registration_info[0]['topics']
        raw_subtopics = user_registration_info[0]['subtopics']

    topics_codes, macro_codes, subtopics_codes  = raw2codes(raw_topics, raw_subtopics)

    return {'topics_codes': topics_codes, 'subtopics_codes': subtopics_codes, 'macro_codes': macro_codes}




def recommendation_loop():
    """
    Questa funzione legge continuamente il file user_actions.json e calcola le raccomandazioni
    basate sulle azioni degli utenti. Le raccomandazioni vengono poi scritte in user_rec.json.
    La funzione si interrompe solo quando viene terminato il processo o quando si verifica un errore.
    La funzione attende 5000 secondi tra un ciclo e l'altro per evitare di sovraccaricare il sistema.

    Il formato atteso per user_actions.json è:
    {
        "paper_id_1": {
            "clicks": ["1"],
            "likes": ["1"],
            "favorites": ["1"],
            "time_spent": [],
            "searches": [],
            "last_active": "2023-10-01T12:00:00"
        },
        "paper_id_2": {
            "clicks": ["0"],
            "likes": ["-1"],
            "favorites": ["0"],
            "time_spent": [],
            "searches": [],
            "last_active": "2023-10-01T12:05:00"
        },
        ...
    }
    """
    while True:
        # leggi il file user_actions.json
        with open('user_actions.json', 'r') as f:
            content = f.read().strip()
            if not content:
                print("Il file user_actions.json è vuoto. Attendo 3 secondi e riprovo...")
                time.sleep(3)
                continue
            user_actions = json.loads(content)
        # se il file non è vuoto, procedo con il calcolo delle raccomandazioni
        print("User actions read successfully. Processing recommendations...")
        # controllo che user_actions sia un dizionario
        if not isinstance(user_actions, dict):
            print("Il file user_actions.json non è un dizionario valido. Attendo 5000 secondi e riprovo...")
            time.sleep(5000)
            continue

        # ristrutturo user_actions in un formato utilizzabile
        user_actions_dict = actions_parsed(user_actions)
        # calcolo le raccomandazioni sulla base del nuovo dizionario user_actions_dict
        recommendations, similar_docs = recommendation_weighted(user_actions_dict)        

        # scrivo le raccomandazioni in un file seguendo il formato di registration_samples.json
        # ossia una lista di dizionari con le chiavi 'id', 'title', 'categories', 'abstract', 'authors', 'published'
        # estratti da df
        recommendations = pd.DataFrame(recommendations)

        # considero gli indici di reccommendations come gli ID degli articoli
        recommendations_ids = recommendations['id'].astype(str)
        # estraggo da df le entry che hanno gli ID presenti in recommendations_ids
        recommendations = df[df['id'].isin(recommendations_ids)]
        
        with open('user_rec.json', 'w') as f:
            json.dump(recommendations.to_dict(orient='records'), f, indent=4)

        time.sleep(30) # Attendo 30 secondi prima di ripetere il ciclo



import os, json
import time 
if __name__ == "__main__":
    global df, df_emb, dataset_ids
    try:
        # Load the dataset and embeddings
        dict_dfs= load_data('/home/justamonkey/Documenti/HACKATHON2025/data/arxiv_dataset.csv', '/home/justamonkey/Documenti/HACKATHON2025/data/arxiv_specter_embeddings.csv')
        df = dict_dfs['df_complete']
        df_emb = dict_dfs['df_emb']
        df_ids_cats = dict_dfs['dataset_ids']
        ##########################################
        print("Dataset and embeddings loaded successfully.")
    except Exception as e:
        print(f"Error loading dataset or embeddings: {e}")
        exit(1)

    # wait user interests from user_registration_info.json
    topics_dict = wait_user_interests()

    macro_codes = topics_dict['macro_codes']
    subtopics_codes = topics_dict['subtopics_codes']

    registration_samples = extract_samples(macro_categories=macro_codes, nsamples=50, sub_categories=subtopics_codes, p_subcat=60, p_randcat=40)

    # write the user interests to a file
    with open('registration_samples.json', 'w') as f:
        json.dump(registration_samples.to_dict(orient='records'), f, indent=4)
    

    print("Waiting for user actions...")
    while not os.path.exists('user_actions.json'):
        pass
    print("User actions file found. Starting recommendation process...")

    # finchè non viene richiamato un segnale di stop, continuo a leggere il file user_actions.json
    recommendation_loop()



    # scrivo delle raccomandazioni basate sulle informazioni contenute dentro user_actions.json
    # aspetto che il file user_actions.json venga modificato