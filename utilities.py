import pandas as pd

# variabili globali che contengono le macro categorie e le sotto categorie
# le macro categorie sono le categorie principali, ad esempio 'cs' per Computer Science, 'econ' per Economics, etc.
# le sotto categorie sono le categorie specifiche all'interno di ogni macro categoria, ad esempio 'cs.AI' per Artificial Intelligence, 'econ.EM' per Econometrics, etc.
# le macro categorie e le sotto categorie sono utilizzate per filtrare gli articoli del dataset in base agli interessi dell'utente
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

# filtra il DataFrame df in base agli interessi dell'utente
# user_interests è una lista di categorie, ad esempio ['cs.AI', 'econ.EM']
# restituisce un DataFrame contenente solo gli articoli che appartengono a una delle categorie specificate
def user_interest_filtering(df, user_interests):
    df_user = df[df['categories'].apply(lambda x: isinstance(x, str) and any(cat in x.split() for cat in user_interests))]
    return df_user


# filtro il dataset in base ai non interessi dell'utente
# df è un DataFrame che contiene gli articoli del dataset
# user_interests è una lista di categorie, ad esempio ['cs.AI', 'econ.EM']
# restituisce un DataFrame contenente n articoli che non appartengono a nessuna delle categorie specificatem 
def random_not_user_interests(df, user_interests, n=20):
    mask = df['categories'].apply(
        lambda x: isinstance(x, str) and not any(cat in x.split() for cat in user_interests)
    )
    df_not_interests = df[mask]
    return df_not_interests.sample(n=min(n, len(df_not_interests)), random_state=42)

# Controlla se le categorie contengono elementi della classe macro_categories
#I codici delle categorie sono stringhe del tipo 'cs.AI', 'econ.EM', etc. in cui la parte prima del punto è la macro categoria e la parte dopo il punto è la sotto categoria.
# Restituisco un DataFrame che contiene solo le righe in cui le categorie contengono la macro categoria specificata.
def check_macro(df, macro_category):
    
    if not isinstance(macro_category, str):
        raise ValueError("macro_category deve essere una stringa.")
    if macro_category not in macro_categories:
        raise ValueError(f"{macro_category} non è una macro categoria valida.")
    
    # estraggo le categorie che contengono la macro categoria
    mask = df['categories'].apply(lambda x: isinstance(x, str) and any(cat.startswith(macro_category + '.') for cat in x.split()))
    return df[mask]