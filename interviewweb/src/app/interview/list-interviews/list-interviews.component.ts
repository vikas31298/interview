import { Component, OnInit } from '@angular/core';

interface Interview {
  interview_id: number;
  company_name: string;
  role_name: string;
  interview_type: string;
  seniority_level: string;
  interview_status: string;
  interview_result: string;
  first_interview_date: string;
  application_date: string;
  total_rounds: number;
  preparation_hours?: number;
}

@Component({
  selector: 'app-list-interviews',
  standalone: false,
  templateUrl: './list-interviews.component.html',
  styleUrl: './list-interviews.component.scss'
})
export class ListInterviewsComponent implements OnInit {
  interviews: Interview[] = [];
  filteredInterviews: Interview[] = [];
  
  // Filter properties
  statusFilter: string = 'all';
  searchTerm: string = '';

  ngOnInit(): void {
    this.loadHardcodedData();
    this.filteredInterviews = [...this.interviews];
  }

  loadHardcodedData(): void {
    this.interviews = [
      {
        interview_id: 1,
        company_name: 'Google',
        role_name: 'Senior Product Manager',
        interview_type: 'actual',
        seniority_level: 'senior',
        interview_status: 'scheduled',
        interview_result: 'pending',
        first_interview_date: '2025-01-15',
        application_date: '2025-01-05',
        total_rounds: 5,
        preparation_hours: 20
      },
      {
        interview_id: 2,
        company_name: 'Meta',
        role_name: 'Technical Product Manager',
        interview_type: 'actual',
        seniority_level: 'senior',
        interview_status: 'in_progress',
        interview_result: 'pending',
        first_interview_date: '2025-01-10',
        application_date: '2024-12-28',
        total_rounds: 4,
        preparation_hours: 15
      },
      {
        interview_id: 3,
        company_name: 'Amazon',
        role_name: 'Product Manager',
        interview_type: 'actual',
        seniority_level: 'mid_level',
        interview_status: 'completed',
        interview_result: 'passed',
        first_interview_date: '2024-12-20',
        application_date: '2024-12-10',
        total_rounds: 4,
        preparation_hours: 18
      },
      {
        interview_id: 4,
        company_name: 'Microsoft',
        role_name: 'GenAI Architect',
        interview_type: 'actual',
        seniority_level: 'senior',
        interview_status: 'scheduled',
        interview_result: 'pending',
        first_interview_date: '2025-01-20',
        application_date: '2025-01-08',
        total_rounds: 5,
        preparation_hours: 25
      },
      {
        interview_id: 5,
        company_name: 'Netflix',
        role_name: 'Product Head',
        interview_type: 'actual',
        seniority_level: 'director',
        interview_status: 'completed',
        interview_result: 'no_hire',
        first_interview_date: '2024-12-15',
        application_date: '2024-12-01',
        total_rounds: 6,
        preparation_hours: 30
      },
      {
        interview_id: 6,
        company_name: 'Apple',
        role_name: 'Senior Technical Product Manager',
        interview_type: 'actual',
        seniority_level: 'senior',
        interview_status: 'in_progress',
        interview_result: 'pending',
        first_interview_date: '2025-01-08',
        application_date: '2024-12-20',
        total_rounds: 5,
        preparation_hours: 22
      },
      {
        interview_id: 7,
        company_name: 'Anthropic',
        role_name: 'GenAI Architect',
        interview_type: 'actual',
        seniority_level: 'staff',
        interview_status: 'scheduled',
        interview_result: 'pending',
        first_interview_date: '2025-01-25',
        application_date: '2025-01-10',
        total_rounds: 4,
        preparation_hours: 28
      },
      {
        interview_id: 8,
        company_name: 'OpenAI',
        role_name: 'Product Manager - AI',
        interview_type: 'actual',
        seniority_level: 'senior',
        interview_status: 'cancelled',
        interview_result: 'unknown',
        first_interview_date: '2025-01-12',
        application_date: '2024-12-30',
        total_rounds: 0,
        preparation_hours: 10
      },
      {
        interview_id: 9,
        company_name: 'Startup XYZ',
        role_name: 'Head of Product',
        interview_type: 'actual',
        seniority_level: 'vp',
        interview_status: 'completed',
        interview_result: 'strong_hire',
        first_interview_date: '2024-12-18',
        application_date: '2024-12-08',
        total_rounds: 3,
        preparation_hours: 12
      },
      {
        interview_id: 10,
        company_name: 'Databricks',
        role_name: 'Data Product Manager',
        interview_type: 'actual',
        seniority_level: 'senior',
        interview_status: 'completed',
        interview_result: 'hire',
        first_interview_date: '2024-12-22',
        application_date: '2024-12-12',
        total_rounds: 4,
        preparation_hours: 16
      }
    ];
  }

  // Filter methods
  filterByStatus(status: string): void {
    this.statusFilter = status;
    this.applyFilters();
  }

  onSearch(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.searchTerm = target.value.toLowerCase();
    this.applyFilters();
  }

  applyFilters(): void {
    this.filteredInterviews = this.interviews.filter(interview => {
      const matchesStatus = this.statusFilter === 'all' || 
                           interview.interview_status === this.statusFilter;
      
      const matchesSearch = !this.searchTerm || 
                           interview.company_name.toLowerCase().includes(this.searchTerm) ||
                           interview.role_name.toLowerCase().includes(this.searchTerm);
      
      return matchesStatus && matchesSearch;
    });
  }

  // Utility methods
  getStatusBadgeClass(status: string): string {
    const statusClasses: { [key: string]: string } = {
      'scheduled': 'badge-info',
      'in_progress': 'badge-warning',
      'completed': 'badge-success',
      'cancelled': 'badge-danger',
      'no_show': 'badge-danger',
      'rescheduled': 'badge-secondary'
    };
    return statusClasses[status] || 'badge-secondary';
  }

  getResultBadgeClass(result: string): string {
    const resultClasses: { [key: string]: string } = {
      'passed': 'badge-success',
      'failed': 'badge-danger',
      'strong_hire': 'badge-success',
      'hire': 'badge-success',
      'no_hire': 'badge-danger',
      'pending': 'badge-warning',
      'mixed': 'badge-secondary',
      'unknown': 'badge-secondary'
    };
    return resultClasses[result] || 'badge-secondary';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  }

  formatInterviewType(type: string): string {
    return type.charAt(0).toUpperCase() + type.slice(1);
  }

  formatSeniorityLevel(level: string): string {
    return level.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  }

  // Navigation methods (placeholder for routing)
  viewDetails(interviewId: number): void {
    console.log('View details for interview:', interviewId);
    // Implement navigation to details page
    // this.router.navigate(['/interviews', interviewId]);
  }

  editInterview(interviewId: number): void {
    console.log('Edit interview:', interviewId);
    // Implement navigation to edit page
  }

  deleteInterview(interviewId: number): void {
    if (confirm('Are you sure you want to delete this interview?')) {
      this.interviews = this.interviews.filter(i => i.interview_id !== interviewId);
      this.applyFilters();
    }
  }

  // Stats
  getTotalInterviews(): number {
    return this.interviews.length;
  }

  getActiveInterviews(): number {
    return this.interviews.filter(i => 
      i.interview_status === 'scheduled' || i.interview_status === 'in_progress'
    ).length;
  }

  getCompletedInterviews(): number {
    return this.interviews.filter(i => i.interview_status === 'completed').length;
  }

  getSuccessRate(): number {
    const completed = this.interviews.filter(i => i.interview_status === 'completed');
    const successful = completed.filter(i => 
      ['passed', 'hire', 'strong_hire'].includes(i.interview_result)
    );
    return completed.length > 0 ? (successful.length / completed.length) * 100 : 0;
  }
}