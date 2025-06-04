import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import random
import numpy as np

macro_categories = {
    "cs": "Computer Science",
    "econ": "Economics",
    "eess": "Electrical Engineering and Systems Science",
    "math": "Mathematics",
    "astro-ph": "Astrophysics",
    "cond-mat": "Condensed Matter",
    "gr-qc": "General Relativity and Quantum Cosmology",
    "hep-ex": "High Energy Physics - Experiment",
    "hep-lat": "High Energy Physics - Lattice",
    "hep-ph": "High Energy Physics - Phenomenology",
    "hep-th": "High Energy Physics - Theory",
    "math-ph": "Mathematical Physics",
    "nlin": "Nonlinear Sciences",
    "nucl-ex": "Nuclear Experiment",
    "nucl-th": "Nuclear Theory",
    "physics": "Physics",
    "quant-ph": "Quantum Physics",
    "q-bio": "Quantitative Biology",
    "q-fin": "Quantitative Finance",
    "stat": "Statistics"
}
sub_categories = {
    "cs": [
        ("cs.AI", "Artificial Intelligence"),
        ("cs.AR", "Hardware Architecture"),
        ("cs.CC", "Computational Complexity"),
        ("cs.CE", "Computational Engineering, Finance, and Science"),
        ("cs.CG", "Computational Geometry"),
        ("cs.CL", "Computation and Language"),
        ("cs.CR", "Cryptography and Security"),
        ("cs.CV", "Computer Vision and Pattern Recognition"),
        ("cs.CY", "Computers and Society"),
        ("cs.DB", "Databases"),
        ("cs.DC", "Distributed, Parallel, and Cluster Computing"),
        ("cs.DL", "Digital Libraries"),
        ("cs.DM", "Discrete Mathematics"),
        ("cs.DS", "Data Structures and Algorithms"),
        ("cs.ET", "Emerging Technologies"),
        ("cs.FL", "Formal Languages and Automata Theory"),
        ("cs.GL", "General Literature"),
        ("cs.GR", "Graphics"),
        ("cs.GT", "Computer Science and Game Theory"),
        ("cs.HC", "Human-Computer Interaction"),
        ("cs.IR", "Information Retrieval"),
        ("cs.IT", "Information Theory"),
        ("cs.LG", "Machine Learning"),
        ("cs.LO", "Logic in Computer Science"),
        ("cs.MA", "Multiagent Systems"),
        ("cs.MM", "Multimedia"),
        ("cs.MS", "Mathematical Software"),
        ("cs.NA", "Numerical Analysis"),
        ("cs.NE", "Neural and Evolutionary Computing"),
        ("cs.NI", "Networking and Internet Architecture"),
        ("cs.OH", "Other Computer Science"),
        ("cs.OS", "Operating Systems"),
        ("cs.PF", "Performance"),
        ("cs.PL", "Programming Languages"),
        ("cs.RO", "Robotics"),
        ("cs.SC", "Symbolic Computation"),
        ("cs.SE", "Software Engineering"),
        ("cs.SI", "Social and Information Networks"),
        ("cs.SY", "Systems and Control"),
    ],
    "econ": [
        ("econ.EM", "Econometrics"),
        ("econ.GN", "General Economics"),
        ("econ.TH", "Theoretical Economics"),
    ],
    "eess": [
        ("eess.AS", "Audio and Speech Processing"),
        ("eess.IV", "Image and Video Processing"),
        ("eess.SP", "Signal Processing"),
        ("eess.SY", "Systems and Control"),
    ],
    "math": [
        ("math.AC", "Commutative Algebra"),
        ("math.AG", "Algebraic Geometry"),
        ("math.AP", "Analysis of PDEs"),
        ("math.AT", "Algebraic Topology"),
        ("math.CA", "Classical Analysis and ODEs"),
        ("math.CO", "Combinatorics"),
        ("math.CT", "Category Theory"),
        ("math.CV", "Complex Variables"),
        ("math.DG", "Differential Geometry"),
        ("math.DS", "Dynamical Systems"),
        ("math.FA", "Functional Analysis"),
        ("math.GM", "General Mathematics"),
        ("math.GN", "General Topology"),
        ("math.GR", "Group Theory"),
        ("math.GT", "Geometric Topology"),
        ("math.HO", "History and Overview"),
        ("math.IT", "Information Theory"),
        ("math.KT", "K-Theory and Homology"),
        ("math.LO", "Logic"),
        ("math.MG", "Metric Geometry"),
        ("math.MP", "Mathematical Physics"),
        ("math.NA", "Numerical Analysis"),
        ("math.NT", "Number Theory"),
        ("math.OA", "Operator Algebras"),
        ("math.OC", "Optimization and Control"),
        ("math.PR", "Probability"),
        ("math.QA", "Quantum Algebra"),
        ("math.RA", "Rings and Algebras"),
        ("math.RT", "Representation Theory"),
        ("math.SG", "Symplectic Geometry"),
        ("math.SP", "Spectral Theory"),
        ("math.ST", "Statistics Theory"),
    ],
    "astro-ph": [
        ("astro-ph.CO", "Cosmology and Nongalactic Astrophysics"),
        ("astro-ph.EP", "Earth and Planetary Astrophysics"),
        ("astro-ph.GA", "Astrophysics of Galaxies"),
        ("astro-ph.HE", "High Energy Astrophysical Phenomena"),
        ("astro-ph.IM", "Instrumentation and Methods for Astrophysics"),
        ("astro-ph.SR", "Solar and Stellar Astrophysics"),
    ],
    "cond-mat": [
        ("cond-mat.dis-nn", "Disordered Systems and Neural Networks"),
        ("cond-mat.mes-hall", "Mesoscale and Nanoscale Physics"),
        ("cond-mat.mtrl-sci", "Materials Science"),
        ("cond-mat.other", "Other Condensed Matter"),
        ("cond-mat.quant-gas", "Quantum Gases"),
        ("cond-mat.soft", "Soft Condensed Matter"),
        ("cond-mat.stat-mech", "Statistical Mechanics"),
        ("cond-mat.str-el", "Strongly Correlated Electrons"),
        ("cond-mat.supr-con", "Superconductivity"),
    ],
    "gr-qc": [
        ("gr-qc", "General Relativity and Quantum Cosmology"),
    ],
    "hep-ex": [
        ("hep-ex", "High Energy Physics - Experiment"),
    ],
    "hep-lat": [
        ("hep-lat", "High Energy Physics - Lattice"),
    ],
    "hep-ph": [
        ("hep-ph", "High Energy Physics - Phenomenology"),
    ],
    "hep-th": [
        ("hep-th", "High Energy Physics - Theory"),
    ],
    "math-ph": [
        ("math-ph", "Mathematical Physics"),
    ],
    "nlin": [
        ("nlin.AO", "Adaptation and Self-Organizing Systems"),
        ("nlin.CD", "Chaotic Dynamics"),
        ("nlin.CG", "Cellular Automata and Lattice Gases"),
        ("nlin.PS", "Pattern Formation and Solitons"),
        ("nlin.SI", "Exactly Solvable and Integrable Systems"),
    ],
    "nucl-ex": [
        ("nucl-ex", "Nuclear Experiment"),
    ],
    "nucl-th": [
        ("nucl-th", "Nuclear Theory"),
    ],
    "physics": [
        ("physics.acc-ph", "Accelerator Physics"),
        ("physics.app-ph", "Applied Physics"),
        ("physics.atm-clus", "Atomic and Molecular Clusters"),
        ("physics.atom-ph", "Atomic Physics"),
        ("physics.bio-ph", "Biological Physics"),
        ("physics.chem-ph", "Chemical Physics"),
        ("physics.class-ph", "Classical Physics"),
        ("physics.comp-ph", "Computational Physics"),
        ("physics.data-an", "Data Analysis, Statistics and Probability"),
        ("physics.ed-ph", "Physics Education"),
        ("physics.flu-dyn", "Fluid Dynamics"),
        ("physics.gen-ph", "General Physics"),
        ("physics.geo-ph", "Geophysics"),
        ("physics.hist-ph", "History and Philosophy of Physics"),
        ("physics.ins-det", "Instrumentation and Detectors"),
        ("physics.med-ph", "Medical Physics"),
        ("physics.optics", "Optics"),
        ("physics.plasm-ph", "Plasma Physics"),
        ("physics.pop-ph", "Popular Physics"),
        ("physics.soc-ph", "Physics and Society"),
        ("physics.space-ph", "Space Physics"),
    ],
    "quant-ph": [
        ("quant-ph", "Quantum Physics"),
    ],
    "q-bio": [
        ("q-bio.BM", "Biomolecules"),
        ("q-bio.CB", "Cell Behavior"),
        ("q-bio.GN", "Genomics"),
        ("q-bio.MN", "Molecular Networks"),
        ("q-bio.NC", "Neurons and Cognition"),
        ("q-bio.OT", "Other Quantitative Biology"),
        ("q-bio.PE", "Populations and Evolution"),
        ("q-bio.QM", "Quantitative Methods"),
        ("q-bio.SC", "Subcellular Processes"),
        ("q-bio.TO", "Tissues and Organs"),
    ],
    "q-fin": [
        ("q-fin.CP", "Computational Finance"),
        ("q-fin.EC", "Economics"),
        ("q-fin.GN", "General Finance"),
        ("q-fin.MF", "Mathematical Finance"),
        ("q-fin.PM", "Portfolio Management"),
        ("q-fin.PR", "Pricing of Securities"),
        ("q-fin.RM", "Risk Management"),
        ("q-fin.ST", "Statistical Finance"),
        ("q-fin.TR", "Trading and Market Microstructure"),
    ],
    "stat": [
        ("stat.AP", "Applications"),
        ("stat.CO", "Computation"),
        ("stat.ME", "Methodology"),
        ("stat.ML", "Machine Learning"),
        ("stat.OT", "Other Statistics"),
        ("stat.TH", "Statistics Theory"),
    ]
}


def load_data(ds_file_path, embeddings_file_path):
    # load the dataset from a CSV file
    print('Loading dataset...')
    df_dataset = pd.read_csv(ds_file_path, usecols=['id', 'categories']) 
    df_emb = pd.read_csv(embeddings_file_path)
    df_emb = df_emb.merge(df_dataset[['id', 'categories']], on='id', how='left')
    print('Dataset loaded successfully.')
    return df_emb

#df = load_data('/Users/enricotazzer/Desktop/hackathon/data/arxiv_dataset.csv', '/Users/enricotazzer/Desktop/hackathon/data/arxiv_specter_embeddings.csv') # Replace with actual file paths

def user_interest_filtering(user_interests):
    df_user = df[df['categories'].apply(lambda x: isinstance(x, str) and any(cat in x.split() for cat in user_interests))]
    return df_user

def random_not_user_interests(df, user_interests, n=20):
    mask = df['categories'].apply(
        lambda x: isinstance(x, str) and not any(cat in x.split() for cat in user_interests)
    )
    df_not_interests = df[mask]
    return df_not_interests.sample(n=min(n, len(df_not_interests)), random_state=42)

def extract_samples(user_interests, n_samples=2):
    samples = []
    for cat in user_interests:
        cat_samples = df[df['categories'].str.contains(cat, na=False)].sample(n=min(n_samples, len(df)), random_state=42)
        samples.append(cat_samples)
    return pd.concat(samples)


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

def code_to_description(code):
    # Macro category
    if code in macro_categories:
        return macro_categories[code]
    # Subcategory
    for macro, subs in sub_categories.items():
        for sub_code, desc in subs:
            if code == sub_code:
                return desc
            
def description_to_code(description):
    # Macro category
    for code, desc in macro_categories.items():
        if desc == description:
            return code
    # Subcategory
    for macro, subs in sub_categories.items():
        for sub_code, desc in subs:
            if desc == description:
                return sub_code



import os, json
if __name__ == "__main__":
    # check if there exist user_registration_info.json
    while not os.path.exists('user_registration_info.json'):
        pass
    with open('user_registration_info.json', 'r') as f:
        user_registration_info = json.load(f)
        raw_topics = user_registration_info['topics']
        topics_codes = code_to_description(raw_topics)
        registration_samples = extract_samples(topics_codes, n_samples=2)
        # write the user interests to a file
        with open('registration_samples.json', 'w') as f:
            json.dump(registration_samples.to_dict(orient='records'), f, indent=4)
    while not os.path.exists('user_actions.json'):
        pass
    while True:
        # scrivo delle raccomandazioni basate sulle informazioni contenute dentro user_actions.json
        # aspetto che il file user_actions.json venga modificato