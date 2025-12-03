import { Component, OnInit, OnDestroy } from '@angular/core';
import { AgentStreamService, StreamEvent, QuestionRequest } from '../services/agent-stream.service';
import { Subject, takeUntil } from 'rxjs';

interface Message {
  role: 'user' | 'agent' | 'system';
  content: string;
  timestamp: Date;
  agentType?: string;
}

@Component({
  selector: 'app-interview-room',
  standalone: false,
  templateUrl: './interview-room.component.html',
  styleUrl: './interview-room.component.scss'
})
export class InterviewRoomComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  question: string = '';
  context: string = '';
  messages: Message[] = [];
  currentAnswer: string = '';
  isStreaming: boolean = false;
  currentAgent: string = '';
  routingReasoning: string = '';
  confidence: number = 0;
  followUpQuestions: string[] = [];
  conversationHistory: any[] = [];

  // Streaming status
  streamingStatus: string = '';
  showRouting: boolean = false;
  showProcessing: boolean = false;

  constructor(private agentStreamService: AgentStreamService) { }

  ngOnInit(): void {
    // Add welcome message
    this.addSystemMessage('Welcome to the AI Interview Room! Ask any interview question and I will help you prepare.');
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Send a question and start streaming the answer
   */
  sendQuestion(): void {
    if (!this.question.trim()) {
      return;
    }

    // Add user message to chat
    this.addUserMessage(this.question);

    // Reset state
    this.currentAnswer = '';
    this.followUpQuestions = [];
    this.isStreaming = true;
    this.showRouting = false;
    this.showProcessing = false;

    const request: QuestionRequest = {
      question: this.question,
      context: this.context || undefined,
      conversation_history: this.conversationHistory
    };

    const currentQuestion = this.question;
    this.question = ''; // Clear input

    // Start streaming
    this.agentStreamService.streamAnswer(request)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (event: StreamEvent) => this.handleStreamEvent(event),
        error: (error) => {
          console.error('Streaming error:', error);
          this.isStreaming = false;
          this.addSystemMessage('Error: Failed to get answer. Please try again.');
        },
        complete: () => {
          this.isStreaming = false;

          // Add to conversation history
          if (this.currentAnswer) {
            this.conversationHistory.push({
              question: currentQuestion,
              answer: this.currentAnswer,
              agent: this.currentAgent
            });
          }
        }
      });
  }

  /**
   * Handle individual stream events
   */
  private handleStreamEvent(event: StreamEvent): void {
    console.log('Stream event:', event.event_type, event.data);

    switch (event.event_type) {
      case 'start':
        this.streamingStatus = event.data.message;
        break;

      case 'routing':
        this.currentAgent = event.data.selected_agent;
        this.routingReasoning = event.data.reasoning;
        this.confidence = event.data.confidence;
        this.showRouting = true;
        this.streamingStatus = `Routed to ${this.formatAgentName(this.currentAgent)} agent`;
        break;

      case 'processing':
        this.showProcessing = true;
        this.streamingStatus = event.data.message;
        break;

      case 'content':
        // Append content chunk to current answer
        this.currentAnswer += event.data.chunk;
        break;

      case 'answer_complete':
        // Finalize answer
        this.currentAnswer = event.data.full_answer;
        this.addAgentMessage(this.currentAnswer, this.currentAgent);
        this.streamingStatus = 'Answer complete';
        break;

      case 'follow_ups':
        this.followUpQuestions = event.data.questions || [];
        break;

      case 'complete':
        this.streamingStatus = 'Complete';
        this.showRouting = false;
        this.showProcessing = false;
        break;

      case 'error':
        this.addSystemMessage(`Error: ${event.data.message}`);
        this.isStreaming = false;
        break;
    }
  }

  /**
   * Ask a follow-up question
   */
  askFollowUp(question: string): void {
    this.question = question;
    this.sendQuestion();
  }

  /**
   * Clear conversation
   */
  clearConversation(): void {
    this.messages = [];
    this.conversationHistory = [];
    this.currentAnswer = '';
    this.followUpQuestions = [];
    this.addSystemMessage('Conversation cleared. Ask a new question to start.');
  }

  /**
   * Add user message to chat
   */
  private addUserMessage(content: string): void {
    this.messages.push({
      role: 'user',
      content: content,
      timestamp: new Date()
    });
  }

  /**
   * Add agent message to chat
   */
  private addAgentMessage(content: string, agentType: string): void {
    this.messages.push({
      role: 'agent',
      content: content,
      timestamp: new Date(),
      agentType: agentType
    });
  }

  /**
   * Add system message to chat
   */
  private addSystemMessage(content: string): void {
    this.messages.push({
      role: 'system',
      content: content,
      timestamp: new Date()
    });
  }

  /**
   * Format agent name for display
   */
  formatAgentName(agentType: string): string {
    return agentType.split('_').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  }

  /**
   * Get agent color for UI
   */
  getAgentColor(agentType: string): string {
    const colors: { [key: string]: string } = {
      'product_manager': '#4CAF50',
      'technical': '#2196F3',
      'architect': '#9C27B0',
      'coding': '#FF9800',
      'behavioral': '#E91E63',
      'system_design': '#00BCD4'
    };
    return colors[agentType] || '#757575';
  }

  /**
   * Handle keyboard event for question input
   */
  onQuestionKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendQuestion();
    }
  }
}
