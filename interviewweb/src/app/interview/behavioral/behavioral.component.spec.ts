import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BehavioralComponent } from './behavioral.component';

describe('BehavioralComponent', () => {
  let component: BehavioralComponent;
  let fixture: ComponentFixture<BehavioralComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BehavioralComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BehavioralComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
