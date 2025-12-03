import { Component, OnInit, OnDestroy } from '@angular/core';
import { AgentStreamService, StreamEvent, QuestionRequest } from '../services/agent-stream.service';
import { Subscription } from 'rxjs';

interface InterviewQuestion {
  id: number;
  question: string;
  category: string;
  difficulty: string;
  topic: string;
  answer: string;
  tips: string[];
  relatedTopics: string[];
  isPracticed: boolean;
}

interface StreamingState {
  isStreaming: boolean;
  selectedAgent?: string;
  routingReasoning?: string;
  confidence?: number;
  streamedAnswer: string;
  fullAnswer?: string;
  followUpQuestions: string[];
  error?: string;
  processingMessage?: string;
}

@Component({
  selector: 'app-search',
  standalone: false,
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss'
})
export class SearchComponent implements OnInit, OnDestroy {
  searchQuery: string = '';
  selectedQuestion: InterviewQuestion | null = null;
  isListening: boolean = false;

  // Streaming state
  streamingState: StreamingState = {
    isStreaming: false,
    streamedAnswer: '',
    followUpQuestions: []
  };

  private streamSubscription?: Subscription;
  private recognition: any;
  private speechSupported: boolean = false;

  // Mock data - replace with actual service call
  allQuestions: InterviewQuestion[] = [
    {
      id: 1,
      question: 'What is the difference between let, const, and var in JavaScript?',
      category: 'JavaScript',
      difficulty: 'Easy',
      topic: 'ES6 Fundamentals',
      answer: 'var is function-scoped and can be redeclared. let is block-scoped and cannot be redeclared in the same scope. const is block-scoped, cannot be redeclared, and its value cannot be reassigned (though object properties can be modified).',
      tips: [
        'Use const by default for immutability',
        'Use let when you need to reassign values',
        'Avoid var in modern JavaScript',
        'Remember block scope vs function scope'
      ],
      relatedTopics: ['Hoisting', 'Scope', 'Temporal Dead Zone'],
      isPracticed: true
    },
    {
      id: 2,
      question: 'Explain the concept of closures in JavaScript',
      category: 'JavaScript',
      difficulty: 'Medium',
      topic: 'Advanced Functions',
      answer: 'A closure is a function that has access to variables in its outer (enclosing) lexical scope, even after the outer function has returned. Closures are created every time a function is created.',
      tips: [
        'Closures remember their lexical environment',
        'Useful for data privacy and encapsulation',
        'Common in callbacks and event handlers',
        'Can lead to memory leaks if not handled properly'
      ],
      relatedTopics: ['Lexical Scope', 'Function Context', 'Memory Management'],
      isPracticed: false
    },
    {
      id: 3,
      question: 'What is the Virtual DOM in React?',
      category: 'React',
      difficulty: 'Medium',
      topic: 'React Core Concepts',
      answer: 'The Virtual DOM is a lightweight copy of the actual DOM. React uses it to optimize updates by comparing the virtual DOM with the real DOM (diffing) and only updating the parts that changed (reconciliation).',
      tips: [
        'Virtual DOM is faster than direct DOM manipulation',
        'React batches updates for better performance',
        'Understanding reconciliation helps optimize React apps',
        'Keys are important for efficient list rendering'
      ],
      relatedTopics: ['Reconciliation', 'React Fiber', 'Performance Optimization'],
      isPracticed: true
    },
    {
      id: 4,
      question: 'Explain the SOLID principles in object-oriented programming',
      category: 'Design Patterns',
      difficulty: 'Hard',
      topic: 'Software Architecture',
      answer: 'SOLID is an acronym: S-Single Responsibility, O-Open/Closed, L-Liskov Substitution, I-Interface Segregation, D-Dependency Inversion. These principles help create maintainable, scalable, and flexible software.',
      tips: [
        'Each class should have one reason to change',
        'Open for extension, closed for modification',
        'Subtypes must be substitutable for base types',
        'Many client-specific interfaces are better than one general interface'
      ],
      relatedTopics: ['Design Patterns', 'Clean Code', 'Dependency Injection'],
      isPracticed: false
    },
    {
      id: 5,
      question: 'What are Promises and async/await in JavaScript?',
      category: 'JavaScript',
      difficulty: 'Medium',
      topic: 'Asynchronous Programming',
      answer: 'Promises represent the eventual completion or failure of an asynchronous operation. async/await is syntactic sugar built on Promises, making asynchronous code look and behave more like synchronous code.',
      tips: [
        'Always handle errors with .catch() or try/catch',
        'Use Promise.all() for parallel operations',
        'async functions always return a Promise',
        'await only works inside async functions'
      ],
      relatedTopics: ['Event Loop', 'Callbacks', 'Error Handling'],
      isPracticed: true
    },
    {
      id: 6,
      question: 'What is the difference between SQL and NoSQL databases?',
      category: 'Databases',
      difficulty: 'Easy',
      topic: 'Database Fundamentals',
      answer: 'SQL databases are relational, use structured schemas, and support ACID transactions. NoSQL databases are non-relational, have flexible schemas, and are designed for horizontal scaling and handling unstructured data.',
      tips: [
        'SQL: MySQL, PostgreSQL, Oracle',
        'NoSQL: MongoDB, Cassandra, Redis',
        'Choose based on data structure and scalability needs',
        'Consider ACID vs BASE consistency models'
      ],
      relatedTopics: ['Database Design', 'Scalability', 'ACID Properties'],
      isPracticed: false
    },
    {
      id: 7,
      question: 'Explain REST API principles and best practices',
      category: 'Web Development',
      difficulty: 'Medium',
      topic: 'API Design',
      answer: 'REST (Representational State Transfer) is an architectural style using HTTP methods (GET, POST, PUT, DELETE) for CRUD operations. Key principles: stateless, client-server separation, cacheable, uniform interface.',
      tips: [
        'Use proper HTTP methods and status codes',
        'Design resource-oriented URLs',
        'Version your APIs (v1, v2)',
        'Implement proper authentication (JWT, OAuth)'
      ],
      relatedTopics: ['HTTP Methods', 'API Security', 'Microservices'],
      isPracticed: true
    },
    {
      id: 8,
      question: 'What is Big O notation and why is it important?',
      category: 'Algorithms',
      difficulty: 'Medium',
      topic: 'Algorithm Analysis',
      answer: 'Big O notation describes the upper bound of time or space complexity of an algorithm. It helps analyze and compare algorithm efficiency as input size grows. Common complexities: O(1), O(log n), O(n), O(n log n), O(n²).',
      tips: [
        'Focus on worst-case scenarios',
        'Drop constants and lower-order terms',
        'Understand space vs time tradeoffs',
        'Practice identifying complexity in code'
      ],
      relatedTopics: ['Time Complexity', 'Space Complexity', 'Algorithm Optimization'],
      isPracticed: false
    }
  ];

  filteredQuestions: InterviewQuestion[] = [];

  constructor(private agentStreamService: AgentStreamService) {}

  ngOnInit(): void {
    this.filteredQuestions = [...this.allQuestions];
    this.initSpeechRecognition();
  }

  ngOnDestroy(): void {
    // Clean up subscription
    if (this.streamSubscription) {
      this.streamSubscription.unsubscribe();
    }
  }

  initSpeechRecognition(): void {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      this.speechSupported = true;
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';

      this.recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        this.searchQuery = transcript;
        this.onSearch();
        this.isListening = false;
      };

      this.recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        this.isListening = false;
      };

      this.recognition.onend = () => {
        this.isListening = false;
      };
    }
  }

  toggleSpeechRecognition(): void {
    if (!this.speechSupported) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    if (this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    } else {
      this.recognition.start();
      this.isListening = true;
    }
  }

  onSearch(): void {
    const query = this.searchQuery.toLowerCase().trim();

    if (!query) {
      this.filteredQuestions = [...this.allQuestions];
      return;
    }

    // Reset streaming state
    this.resetStreamingState();

    // Start streaming answer from API
    this.streamAnswerFromAPI(query);
  }

  private resetStreamingState(): void {
    this.streamingState = {
      isStreaming: true,
      streamedAnswer: '',
      followUpQuestions: []
    };

    // Unsubscribe from previous stream if exists
    if (this.streamSubscription) {
      this.streamSubscription.unsubscribe();
    }
  }

  private streamAnswerFromAPI(question: string): void {
    const request: QuestionRequest = {
      question: question,
      context: 'User searching for interview question answer',
      conversation_history: []
    };

    this.streamSubscription = this.agentStreamService.streamAnswer(request).subscribe({
      next: (event: StreamEvent) => this.handleStreamEvent(event),
      error: (error) => this.handleStreamError(error),
      complete: () => this.handleStreamComplete()
    });
  }

  private handleStreamEvent(event: StreamEvent): void {
    console.log('Stream event:', event);

    switch (event.event_type) {
      case 'start':
        this.streamingState.processingMessage = event.data.message;
        break;

      case 'routing':
        this.streamingState.selectedAgent = event.data.selected_agent;
        this.streamingState.routingReasoning = event.data.reasoning;
        this.streamingState.confidence = event.data.confidence;
        break;

      case 'processing':
        this.streamingState.processingMessage = event.data.message;
        break;

      case 'content':
        // Append chunk to streamed answer
        this.streamingState.streamedAnswer += event.data.chunk;
        break;

      case 'answer_complete':
        this.streamingState.fullAnswer = event.data.full_answer;
        this.streamingState.streamedAnswer = event.data.full_answer;
        break;

      case 'follow_ups':
        this.streamingState.followUpQuestions = event.data.questions || [];
        break;

      case 'complete':
        this.streamingState.isStreaming = false;
        break;

      case 'error':
        this.streamingState.error = event.data.error || event.data.message;
        this.streamingState.isStreaming = false;
        break;
    }
  }

  private handleStreamError(error: any): void {
    console.error('Stream error:', error);
    this.streamingState.error = 'Failed to get answer from API. Please try again.';
    this.streamingState.isStreaming = false;
  }

  private handleStreamComplete(): void {
    console.log('Stream complete');
    this.streamingState.isStreaming = false;
  }

  selectFollowUpQuestion(question: string): void {
    this.searchQuery = question;
    this.onSearch();
  }

  selectQuestion(question: InterviewQuestion): void {
    this.selectedQuestion = question;
  }

  clearSelection(): void {
    this.selectedQuestion = null;
  }

  getDifficultyClass(difficulty: string): string {
    return difficulty.toLowerCase();
  }

  getCategoryClass(category: string): string {
    return category.toLowerCase().replace(/\s+/g, '-');
  }

  togglePracticed(question: InterviewQuestion): void {
    question.isPracticed = !question.isPracticed;
    // TODO: Persist this change to backend/local storage
  }
}
