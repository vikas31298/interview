import { Injectable } from '@angular/core';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

export interface StreamEvent {
  event_type: 'start' | 'routing' | 'processing' | 'content' | 'answer_complete' | 'follow_ups' | 'complete' | 'error';
  timestamp: string;
  data: any;
}

export interface QuestionRequest {
  question: string;
  context?: string;
  conversation_history?: any[];
}

@Injectable({
  providedIn: 'root'
})
export class AgentStreamService {
  private apiUrl = 'http://localhost:8000/api/agents';

  constructor(private http: HttpClient) { }

  /**
   * Stream answer from the agent using Server-Sent Events (SSE)
   * Returns an Observable of StreamEvent objects
   */
  streamAnswer(request: QuestionRequest): Observable<StreamEvent> {
    const subject = new Subject<StreamEvent>();

    this.http.post(`${this.apiUrl}/answer-stream`, request, {
      observe: 'events',
      responseType: 'text',
      reportProgress: true
    }).subscribe({
      next: (event: any) => {
        if (event.type === HttpEventType.DownloadProgress) {
          // Parse the partial text for SSE events
          const text = event.partialText || '';
          const lines = text.split('\n\n');

          lines.forEach((line: string) => {
            if (line.startsWith('data: ')) {
              try {
                const jsonData = line.substring(6); // Remove 'data: ' prefix
                const parsedEvent: StreamEvent = JSON.parse(jsonData);
                subject.next(parsedEvent);
              } catch (e) {
                console.error('Error parsing SSE event:', e);
              }
            }
          });
        } else if (event.type === HttpEventType.Response) {
          // Stream completed
          subject.complete();
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
   * Get complete answer without streaming (fallback method)
   */
  getAnswer(request: QuestionRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/answer`, request);
  }

  /**
   * Get list of available agents
   */
  getAvailableAgents(): Observable<any> {
    return this.http.get(`${this.apiUrl}/available`);
  }
}
