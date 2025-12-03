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
  selector: 'app-frequent',
  standalone: false,
  templateUrl: './frequent.component.html',
  styleUrl: './frequent.component.scss'
})
export class FrequentComponent implements OnInit, OnDestroy {
  searchQuery: string = '';
  selectedQuestion: InterviewQuestion | null = null;
  isListening: boolean = false;

  streamingState: StreamingState = {
    isStreaming: false,
    streamedAnswer: '',
    followUpQuestions: []
  };

  private streamSubscription?: Subscription;
  private recognition: any;
  private speechSupported: boolean = false;

  allQuestions: InterviewQuestion[] = [];
  filteredQuestions: InterviewQuestion[] = [];

  constructor(private agentStreamService: AgentStreamService) {}

  ngOnInit(): void {
    this.filteredQuestions = [...this.allQuestions];
    this.initSpeechRecognition();
  }

  ngOnDestroy(): void {
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
    this.resetStreamingState();
    this.streamAnswerFromAPI(query);
  }

  private resetStreamingState(): void {
    this.streamingState = {
      isStreaming: true,
      streamedAnswer: '',
      followUpQuestions: []
    };
    if (this.streamSubscription) {
      this.streamSubscription.unsubscribe();
    }
  }

  private streamAnswerFromAPI(question: string): void {
    const request: QuestionRequest = {
      question: question,
      context: 'Frequent interview questions',
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
  }
}
