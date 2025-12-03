import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-interview',
  standalone: false,
  templateUrl: './add-interview.component.html',
  styleUrl: './add-interview.component.scss'
})
export class AddInterviewComponent implements OnInit {
  interviewForm!: FormGroup;
  submitted = false;

  interviewTypes = [
    { value: 'technical', label: 'Technical Interview' },
    { value: 'hr', label: 'HR Interview' },
    { value: 'behavioral', label: 'Behavioral Interview' },
    { value: 'coding', label: 'Coding Interview' },
    { value: 'system-design', label: 'System Design' }
  ];

  experienceLevels = [
    { value: 'entry', label: 'Entry Level (0-2 years)' },
    { value: 'intermediate', label: 'Intermediate (2-5 years)' },
    { value: 'senior', label: 'Senior (5-10 years)' },
    { value: 'expert', label: 'Expert (10+ years)' }
  ];

  constructor(
    private formBuilder: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.interviewForm = this.formBuilder.group({
      candidateName: ['', [Validators.required, Validators.minLength(2)]],
      candidateEmail: ['', [Validators.required, Validators.email]],
      position: ['', [Validators.required, Validators.minLength(2)]],
      interviewType: ['', Validators.required],
      experienceLevel: ['', Validators.required],
      scheduledDate: ['', Validators.required],
      scheduledTime: ['', Validators.required],
      duration: [60, [Validators.required, Validators.min(15), Validators.max(240)]],
      interviewerName: ['', Validators.required],
      interviewerEmail: ['', [Validators.required, Validators.email]],
      notes: [''],
      location: ['']
    });
  }

  get f() {
    return this.interviewForm.controls;
  }

  onSubmit(): void {
    this.submitted = true;

    if (this.interviewForm.invalid) {
      return;
    }

    console.log('Interview Details:', this.interviewForm.value);

    // TODO: Add service call to save interview
    alert('Interview scheduled successfully!');

    this.router.navigate(['/interview/list']);
  }

  onReset(): void {
    this.submitted = false;
    this.interviewForm.reset({
      duration: 60
    });
  }

  onCancel(): void {
    this.router.navigate(['/interview/list']);
  }
}
