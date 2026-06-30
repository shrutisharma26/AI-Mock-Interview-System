

REFERENCE_ANSWERS = {

    # ================= SDE - EASY =================

    "Explain time complexity.": (
        "Time complexity measures the amount of time an algorithm takes "
        "to execute as the input size grows. It is usually expressed using "
        "Big O notation such as O(1), O(log n), O(n), O(n log n), or O(n²). "
        "It helps compare the efficiency and scalability of algorithms."
    ),

    "What is a queue?": (
        "A queue is a linear data structure that follows the FIFO "
        "(First In First Out) principle. Elements are inserted at the rear "
        "using enqueue operation and removed from the front using dequeue "
        "operation. Queues are used in scheduling, buffering, and BFS."
    ),

    "What is the difference between an array and a linked list?": (
        "An array stores elements in contiguous memory locations and "
        "supports constant time random access. A linked list stores nodes "
        "using pointers and does not require contiguous memory. Arrays "
        "have fixed size while linked lists allow dynamic insertion and deletion."
    ),

    "Explain OOP principles.": (
        "The four main principles of Object Oriented Programming are "
        "Encapsulation, Abstraction, Inheritance, and Polymorphism. "
        "Encapsulation hides implementation details, abstraction exposes only "
        "essential features, inheritance promotes code reuse, and polymorphism "
        "allows the same interface to behave differently."
    ),

    "What is recursion?": (
        "Recursion is a programming technique in which a function calls "
        "itself to solve smaller subproblems. Every recursive function must "
        "have a base case to stop recursion and a recursive case that reduces "
        "the problem size."
    ),

    # ================= SDE - MEDIUM =================

    "Explain HashMap internals.": (
        "A HashMap stores key-value pairs using an array of buckets. "
        "Keys are hashed to determine the bucket index. Collisions are "
        "handled using linked lists or balanced trees in modern implementations. "
        "Average time complexity for insertion, deletion, and search is O(1)."
    ),

    "What is Dynamic Programming?": (
        "Dynamic Programming is an optimization technique used to solve "
        "overlapping subproblems with optimal substructure. It stores results "
        "of previously solved subproblems using memoization or tabulation to "
        "avoid redundant computations."
    ),

    "How does Merge Sort work?": (
        "Merge Sort is a divide and conquer algorithm. It recursively divides "
        "the array into halves until single elements remain and then merges "
        "the sorted halves. Its time complexity is O(n log n) and it requires "
        "additional auxiliary space."
    ),

    "Explain Binary Search Tree.": (
        "A Binary Search Tree is a binary tree in which the left subtree "
        "contains values smaller than the root and the right subtree contains "
        "values greater than the root. Search, insertion, and deletion "
        "operations take O(log n) time in a balanced BST."
    ),

    "What is a Heap?": (
        "A heap is a complete binary tree that satisfies the heap property. "
        "In a max heap, the parent node is greater than its children, while "
        "in a min heap, the parent is smaller. Heaps are commonly used in "
        "priority queues and heap sort."
    ),

    # ================= SDE - HARD =================

    "Design an LRU Cache.": (
        "An LRU Cache evicts the least recently used item when capacity is "
        "exceeded. It can be efficiently implemented using a combination of "
        "a hash map and a doubly linked list. Both get and put operations "
        "can be performed in O(1) time."
    ),

    "Explain Dijkstra's Algorithm.": (
        "Dijkstra's Algorithm finds the shortest path from a source node "
        "to all other nodes in a weighted graph with non-negative weights. "
        "It uses a priority queue to repeatedly select the node with minimum "
        "distance and relax its adjacent edges."
    ),

    "What is Segment Tree?": (
        "A Segment Tree is a tree-based data structure used for efficient "
        "range queries and updates on arrays. It supports operations such as "
        "range sum, minimum, and maximum queries in O(log n) time."
    ),

    "Design a scalable URL shortener.": (
        "A scalable URL shortener requires components such as load balancers, "
        "databases, caching, unique ID generation, and distributed systems. "
        "The system should ensure high availability, scalability, low latency, "
        "and efficient storage of short and long URLs."
    ),

    "Explain Red-Black Trees.": (
        "A Red-Black Tree is a self-balancing binary search tree in which "
        "every node is colored red or black. It maintains balance using "
        "rotation and recoloring rules, ensuring O(log n) time complexity "
        "for insertion, deletion, and search."
    ),

    # ================= ML - EASY =================

    "What is overfitting?": (
        "Overfitting occurs when a machine learning model learns noise and "
        "training data too well, resulting in poor generalization on unseen "
        "data. Techniques such as regularization, cross-validation, and "
        "dropout can reduce overfitting."
    ),

    "What is bias and variance?": (
        "Bias refers to errors due to overly simplistic assumptions in a model, "
        "while variance refers to sensitivity to training data fluctuations. "
        "A good model achieves a balance between bias and variance."
    ),

    "Explain train-test split.": (
        "Train-test split divides a dataset into training and testing sets. "
        "The training set is used to train the model, while the testing set "
        "evaluates model performance on unseen data."
    ),

    # ================= ML - MEDIUM =================

    "Explain Random Forest.": (
        "Random Forest is an ensemble learning algorithm that builds multiple "
        "decision trees using random subsets of data and features. Predictions "
        "from all trees are combined using voting or averaging to improve accuracy."
    ),

    "What is Gradient Descent?": (
        "Gradient Descent is an optimization algorithm used to minimize a loss "
        "function by iteratively updating model parameters in the direction of "
        "the negative gradient."
    ),

    "How does SVM work?": (
        "Support Vector Machine is a supervised learning algorithm that finds "
        "the optimal hyperplane maximizing the margin between classes. Kernels "
        "allow SVMs to solve non-linear classification problems."
    ),

    # ================= ML - HARD =================

    "Explain Transformers.": (
        "Transformers are deep learning architectures based on self-attention "
        "mechanisms. They process input sequences in parallel and are widely "
        "used in NLP tasks such as translation, summarization, and large language models."
    ),

    "What is XGBoost?": (
        "XGBoost is an optimized gradient boosting algorithm that builds "
        "decision trees sequentially to minimize errors. It supports "
        "regularization, parallel processing, and efficient handling of large datasets."
    ),

    "Explain Attention Mechanism.": (
        "Attention Mechanism allows neural networks to focus on important parts "
        "of the input while making predictions. Self-attention computes relationships "
        "between all elements in a sequence and is a core component of Transformers."
    ),

    # ================= DS - EASY =================

    "What is Pandas?": (
        "Pandas is a Python library for data manipulation and analysis. "
        "It provides data structures such as DataFrame and Series for handling "
        "structured data efficiently."
    ),

    "What is data cleaning?": (
        "Data cleaning is the process of detecting and correcting inaccurate, "
        "missing, duplicate, or inconsistent data to improve data quality before analysis."
    ),

    "Explain missing values.": (
        "Missing values occur when data is unavailable for certain observations. "
        "Common methods to handle missing values include deletion, mean or median "
        "imputation, and predictive modeling."
    ),

    # ================= DS - MEDIUM =================

    "Explain PCA.": (
        "Principal Component Analysis is a dimensionality reduction technique "
        "that transforms correlated variables into a smaller number of "
        "uncorrelated principal components while preserving maximum variance."
    ),

    "What is feature engineering?": (
        "Feature engineering involves creating, selecting, and transforming "
        "variables to improve machine learning model performance."
    ),

    "What is hypothesis testing?": (
        "Hypothesis testing is a statistical method used to determine whether "
        "there is enough evidence to reject a null hypothesis in favor of an alternative hypothesis."
    ),

    # ================= DS - HARD =================

    "Explain A/B testing.": (
        "A/B testing compares two versions of a product, webpage, or feature "
        "to determine which performs better based on predefined metrics and statistical significance."
    ),

    "What is bootstrapping?": (
        "Bootstrapping is a resampling technique that repeatedly samples data "
        "with replacement to estimate statistics such as confidence intervals."
    ),

    "Explain dimensionality reduction.": (
        "Dimensionality reduction reduces the number of input features while "
        "preserving important information. Techniques include PCA, t-SNE, and Autoencoders."
    )
}