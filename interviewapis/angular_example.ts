/**
 * Angular Service Example for Consuming Streaming Interview API
 *
 * This service demonstrates how to consume the Server-Sent Events (SSE)
 * streaming API from an Angular application.
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

// ============================================================================
// INTERFACES
// ============================================================================

export interface QuestionRequest {
  question: string;
  context?: string;
  conversation_history?: Array<{ role: string; content: string }>;
}

export interface StreamEvent {
  event_type: 'start' | 'routing' | 'processing' | 'content' | 'answer_complete' | 'follow_ups' | 'complete' | 'error';
  timestamp: string;
  data: any;
}

export interface AnswerResponse {
  success: boolean;
  timestamp: string;
  question: string;
  routing: {
    selected_agent: string;
    reasoning: string;
    confidence: number;
  };
  answer: string;
  metadata: any;
  follow_up_questions: string[];
  statistics: {
    word_count: number;
    character_count: number;
  };
}

// ============================================================================
// ANGULAR SERVICE
// ============================================================================

@Injectable({
  providedIn: 'root'
})
export class InterviewService {

  private apiUrl = 'http://localhost:8000/api/agents';

  constructor(private http: HttpClient) {}

  /**
   * METHOD 1: Stream interview answer using HttpClient (Recommended for Angular)
   *
   * This method uses HttpClient with text streaming to consume SSE.
   * It's the most Angular-friendly approach.
   */
  streamAnswer(request: QuestionRequest): Observable<StreamEvent> {
    const subject = new Subject<StreamEvent>();
    let buffer = '';

    this.http.post(`${this.apiUrl}/answer-stream`, request, {
      observe: 'events',
      responseType: 'text',
      reportProgress: true
    }).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.DownloadProgress) {
          // Accumulate chunks
          buffer += (event as any).partialText || '';

          // Process complete events
          const events = buffer.split('\n\n');
          buffer = events.pop() || ''; // Keep incomplete event in buffer

          events.forEach(eventStr => {
            if (eventStr.trim().startsWith('data: ')) {
              try {
                const jsonData = eventStr.substring(6); // Remove "data: " prefix
                const streamEvent: StreamEvent = JSON.parse(jsonData);
                subject.next(streamEvent);
              } catch (e) {
                console.error('Failed to parse SSE event:', e);
              }
            }
          });
        }
      },
      error: (error) => {
        subject.error(error);
      },
      complete: () => {
        subject.complete();
      }
    });

    return subject.asObservable();
  }

  /**
   * METHOD 2: Get complete answer without streaming
   *
   * Use this when you don't need real-time streaming and want
   * the complete response at once.
   */
  getAnswer(request: QuestionRequest): Observable<AnswerResponse> {
    return this.http.post<AnswerResponse>(`${this.apiUrl}/answer`, request);
  }

  /**
   * Get list of available agents
   */
  getAvailableAgents(): Observable<any> {
    return this.http.get(`${this.apiUrl}/available`);
  }
}


// ============================================================================
// ANGULAR COMPONENT EXAMPLE
// ============================================================================

/**
 * Example Component showing how to use the streaming service
 */

import { Component } from '@angular/core';

@Component({
  selector: 'app-interview-chat',
  template: `
    <div class="interview-container">
      <h2>Interview Question Assistant</h2>

      <!-- Question Input -->
      <div class="question-input">
        <textarea
          [(ngModel)]="question"
          placeholder="Enter your interview question..."
          rows="4"
        ></textarea>

        <button
          (click)="askQuestion()"
          [disabled]="isProcessing || !question"
        >
          {{ isProcessing ? 'Processing...' : 'Ask Question' }}
        </button>
      </div>

      <!-- Routing Information -->
      <div class="routing-info" *ngIf="routingInfo">
        <h4>Routing Information</h4>
        <p><strong>Selected Agent:</strong> {{ routingInfo.selected_agent }}</p>
        <p><strong>Confidence:</strong> {{ routingInfo.confidence * 100 }}%</p>
        <p><strong>Reasoning:</strong> {{ routingInfo.reasoning }}</p>
      </div>

      <!-- Streaming Answer -->
      <div class="answer-container" *ngIf="answer">
        <h4>Answer</h4>
        <div class="answer-content" [innerHTML]="answer"></div>
        <div class="streaming-indicator" *ngIf="isStreaming">
          <span class="pulse">●</span> Streaming...
        </div>
      </div>

      <!-- Follow-up Questions -->
      <div class="follow-ups" *ngIf="followUpQuestions.length > 0">
        <h4>Follow-up Questions</h4>
        <ul>
          <li *ngFor="let q of followUpQuestions" (click)="askFollowUp(q)">
            {{ q }}
          </li>
        </ul>
      </div>

      <!-- Error Display -->
      <div class="error" *ngIf="error">
        <strong>Error:</strong> {{ error }}
      </div>
    </div>
  `,
  styles: [`
    .interview-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }

    .question-input {
      margin-bottom: 20px;
    }

    textarea {
      width: 100%;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 14px;
    }

    button {
      margin-top: 10px;
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    button:disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }

    .routing-info {
      background-color: #f8f9fa;
      padding: 15px;
      border-radius: 4px;
      margin-bottom: 20px;
    }

    .answer-container {
      background-color: #fff;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 15px;
      margin-bottom: 20px;
    }

    .answer-content {
      line-height: 1.6;
      white-space: pre-wrap;
    }

    .streaming-indicator {
      margin-top: 10px;
      color: #007bff;
    }

    .pulse {
      animation: pulse 1s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }

    .follow-ups {
      background-color: #e9ecef;
      padding: 15px;
      border-radius: 4px;
    }

    .follow-ups ul {
      list-style: none;
      padding: 0;
    }

    .follow-ups li {
      padding: 10px;
      margin: 5px 0;
      background-color: white;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .follow-ups li:hover {
      background-color: #f8f9fa;
    }

    .error {
      background-color: #f8d7da;
      color: #721c24;
      padding: 15px;
      border-radius: 4px;
      margin-top: 20px;
    }
  `]
})
export class InterviewChatComponent {
  question = '';
  answer = '';
  routingInfo: any = null;
  followUpQuestions: string[] = [];
  isProcessing = false;
  isStreaming = false;
  error: string | null = null;

  constructor(private interviewService: InterviewService) {}

  askQuestion() {
    if (!this.question.trim()) return;

    this.resetState();
    this.isProcessing = true;
    this.isStreaming = true;

    const request: QuestionRequest = {
      question: this.question,
      context: 'Senior engineer with 5 years experience'
    };

    this.interviewService.streamAnswer(request).subscribe({
      next: (event: StreamEvent) => {
        this.handleStreamEvent(event);
      },
      error: (error) => {
        this.error = error.message || 'An error occurred';
        this.isProcessing = false;
        this.isStreaming = false;
      },
      complete: () => {
        this.isProcessing = false;
        this.isStreaming = false;
      }
    });
  }

  handleStreamEvent(event: StreamEvent) {
    console.log('Stream event:', event);

    switch (event.event_type) {
      case 'start':
        console.log('Processing started:', event.data.message);
        break;

      case 'routing':
        this.routingInfo = event.data;
        break;

      case 'processing':
        console.log('Processing:', event.data.message);
        break;

      case 'content':
        // Append content chunk to answer
        this.answer += event.data.chunk;
        break;

      case 'answer_complete':
        // Ensure we have the full answer
        this.answer = event.data.full_answer;
        console.log('Answer complete:', event.data.word_count, 'words');
        break;

      case 'follow_ups':
        this.followUpQuestions = event.data.questions;
        break;

      case 'complete':
        console.log('Processing complete');
        break;

      case 'error':
        this.error = event.data.message;
        break;
    }
  }

  askFollowUp(question: string) {
    this.question = question;
    this.askQuestion();
  }

  resetState() {
    this.answer = '';
    this.routingInfo = null;
    this.followUpQuestions = [];
    this.error = null;
  }
}


// ============================================================================
// ALTERNATIVE: Using Native EventSource (Browser API)
// ============================================================================

/**
 * This is an alternative approach using the native EventSource API.
 * However, EventSource doesn't support POST requests by default,
 * so you'd need to encode the question in the URL or use a library.
 *
 * The HttpClient approach above is recommended for Angular.
 */

/*
export class InterviewServiceEventSource {

  streamAnswerWithEventSource(question: string): Observable<StreamEvent> {
    return new Observable(observer => {
      // Note: EventSource only supports GET requests
      // You'd need to encode the question in the URL
      const encodedQuestion = encodeURIComponent(question);
      const eventSource = new EventSource(
        `http://localhost:8000/api/agents/answer-stream?question=${encodedQuestion}`
      );

      eventSource.onmessage = (event) => {
        try {
          const data: StreamEvent = JSON.parse(event.data);
          observer.next(data);
        } catch (e) {
          observer.error(e);
        }
      };

      eventSource.onerror = (error) => {
        observer.error(error);
        eventSource.close();
      };

      // Cleanup
      return () => {
        eventSource.close();
      };
    });
  }
}
*/


// ============================================================================
// MODULE SETUP
// ============================================================================

/**
 * Don't forget to add HttpClientModule to your Angular module:
 *
 * import { HttpClientModule } from '@angular/common/http';
 * import { FormsModule } from '@angular/forms';
 *
 * @NgModule({
 *   imports: [
 *     HttpClientModule,
 *     FormsModule
 *   ]
 * })
 */
