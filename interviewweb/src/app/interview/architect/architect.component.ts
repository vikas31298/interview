import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

interface ArchitectPattern {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  contentType: 'markdown' | 'image' | 'html';
  markdownFile?: string;
  imageUrl?: string;
  htmlFile?: string;
  tags: string[];
  color: string;
}

@Component({
  selector: 'app-architect',
  standalone: false,
  templateUrl: './architect.component.html',
  styleUrl: './architect.component.scss'
})
export class ArchitectComponent implements OnInit {
  architectPatterns: ArchitectPattern[] = [];
  filteredPatterns: ArchitectPattern[] = [];
  paginatedPatterns: ArchitectPattern[] = [];
  selectedPattern: ArchitectPattern | null = null;
  markdownContent: string = '';
  htmlContent: string = '';
  isLoading: boolean = false;
  error: string = '';
  searchQuery: string = '';
  selectedCategory: string = 'all';

  // Pagination properties
  currentPage: number = 1;
  itemsPerPage: number = 6;
  totalPages: number = 1;

  categories: string[] = [];

  constructor(
    private http: HttpClient,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.loadPatternsFromJson();
  }

  loadPatternsFromJson(): void {
    this.isLoading = true;
    this.http.get<ArchitectPattern[]>('assets/data/architect-patterns.json')
      .subscribe({
        next: (data) => {
          this.architectPatterns = data;
          this.filteredPatterns = [...this.architectPatterns];
          this.extractCategories();
          this.updatePagination();
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error loading patterns:', err);
          this.error = 'Failed to load architecture patterns';
          this.isLoading = false;
        }
      });
  }

  extractCategories(): void {
    const categorySet = new Set(this.architectPatterns.map(p => p.category));
    this.categories = Array.from(categorySet);
  }

  updatePagination(): void {
    this.totalPages = Math.ceil(this.filteredPatterns.length / this.itemsPerPage);
    
    // Reset to page 1 if current page exceeds total pages
    if (this.currentPage > this.totalPages) {
      this.currentPage = 1;
    }

    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.paginatedPatterns = this.filteredPatterns.slice(startIndex, endIndex);
  }

  selectPattern(pattern: ArchitectPattern): void {
    this.selectedPattern = pattern;
    this.error = '';
    this.markdownContent = '';
    this.htmlContent = '';
    
    if (pattern.contentType === 'markdown' && pattern.markdownFile) {
      this.loadMarkdownFile(pattern.markdownFile);
    } else if (pattern.contentType === 'html' && pattern.htmlFile) {
      this.loadHtmlFile(pattern.htmlFile);
    }
  }

  loadMarkdownFile(filename: string): void {
    this.isLoading = true;
    const filePath = `answers/architect/${filename}`;
    
    this.http.get(filePath, { responseType: 'text' })
      .subscribe({
        next: (data) => {
          this.markdownContent = data;
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error loading markdown file:', err);
          this.error = `Failed to load ${filename}`;
          this.isLoading = false;
        }
      });
  }

  loadHtmlFile(filename: string): void {
    this.isLoading = true;
    const filePath = `answers/architect/${filename}`;
    
    this.http.get(filePath, { responseType: 'text' })
      .subscribe({
        next: (data) => {
          this.htmlContent = data;
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error loading HTML file:', err);
          this.error = `Failed to load ${filename}`;
          this.isLoading = false;
        }
      });
  }

  clearSelection(): void {
    this.selectedPattern = null;
    this.markdownContent = '';
    this.htmlContent = '';
    this.error = '';
  }

  filterPatterns(): void {
    this.filteredPatterns = this.architectPatterns.filter(pattern => {
      const matchesSearch = !this.searchQuery || 
        pattern.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        pattern.description.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        pattern.tags.some(tag => tag.toLowerCase().includes(this.searchQuery.toLowerCase()));
      
      const matchesCategory = this.selectedCategory === 'all' || pattern.category === this.selectedCategory;
      
      return matchesSearch && matchesCategory;
    });

    // Reset to page 1 when filters change
    this.currentPage = 1;
    this.updatePagination();
  }

  onSearchChange(): void {
    this.filterPatterns();
  }

  onCategoryChange(category: string): void {
    this.selectedCategory = category;
    this.filterPatterns();
  }

  // Pagination methods
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.updatePagination();
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updatePagination();
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updatePagination();
    }
  }

  getPageNumbers(): number[] {
    const pages: number[] = [];
    const maxVisiblePages = 5;
    
    if (this.totalPages <= maxVisiblePages) {
      // Show all pages if total is less than max visible
      for (let i = 1; i <= this.totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Show subset with ellipsis logic
      if (this.currentPage <= 3) {
        for (let i = 1; i <= 4; i++) pages.push(i);
        pages.push(-1); // Ellipsis
        pages.push(this.totalPages);
      } else if (this.currentPage >= this.totalPages - 2) {
        pages.push(1);
        pages.push(-1); // Ellipsis
        for (let i = this.totalPages - 3; i <= this.totalPages; i++) pages.push(i);
      } else {
        pages.push(1);
        pages.push(-1); // Ellipsis
        pages.push(this.currentPage - 1);
        pages.push(this.currentPage);
        pages.push(this.currentPage + 1);
        pages.push(-1); // Ellipsis
        pages.push(this.totalPages);
      }
    }
    
    return pages;
  }

  getCategoryClass(category: string): string {
    return category.toLowerCase().replace(/\s+/g, '-');
  }

  getDifficultyClass(difficulty: string): string {
    return difficulty.toLowerCase();
  }
}