const API_BASE_URL = 'http://localhost:8001';

export interface Company {
  id: number;
  name: string;
  email: string;
  domain?: string;
  max_users: number;
  is_active: boolean;
  created_by: number;
  created_by_name?: string;
  created_at: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
  company_id: number | null;
  company_name?: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  company_id?: number;
}

export interface OTPVerifyRequest {
  email: string;
  otp: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CompanyCreateRequest {
  name: string;
  email: string;
  domain?: string;
  max_users?: number;
}

export interface UserCreateRequest {
  email: string;
  role: string;
}

export interface AppointmentCreateRequest {
  employee_name: string;
  department: string;
  reason?: string;
  appointment_date: string;
  appointment_time: string;
  visitor_name: string;
  visitor_email: string;
  visitor_phone?: string;
  booking_method?: string;
}

export interface Employee {
  id: number;
  name: string;
  email: string;
  department: string;
  designation?: string;
  phone?: string;
  is_active: boolean;
  created_at: string;
}

export interface EmployeeCreate {
  name: string;
  email: string;
  department: string;
  designation?: string;
  phone?: string;
}

export interface Appointment {
  id: number;
  employee_name: string;
  department: string;
  reason?: string;
  appointment_date: string;
  appointment_time: string;
  visitor_name: string;
  visitor_email: string;
  visitor_phone?: string;
  company_id: number;
  company_name?: string;
  booking_method: string;
  status: string;
  qr_code_sent: boolean;
  email_sent: boolean;
  created_at: string;
  updated_at: string;
}

export interface AppointmentUpdateRequest {
  status: string;
}

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');
    console.log('Token from localStorage:', token ? `${token.substring(0, 20)}...` : 'null');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  // Superadmin endpoints
  async superadminLogin(email: string): Promise<{ message: string; email: string }> {
    const response = await fetch(`${API_BASE_URL}/superadmin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to send OTP');
    }
    
    return response.json();
  }

  async superadminVerifyOTP(email: string, otp: string): Promise<TokenResponse> {
    const response = await fetch(`${API_BASE_URL}/superadmin/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp }),
    });
    
    if (!response.ok) {
      throw new Error('Invalid OTP');
    }
    
    return response.json();
  }

  async createCompany(company: CompanyCreateRequest): Promise<Company> {
    const response = await fetch(`${API_BASE_URL}/superadmin/companies`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(company),
    });
    
    if (!response.ok) {
      throw new Error('Failed to create company');
    }
    
    return response.json();
  }

  async getCompanies(): Promise<Company[]> {
    const response = await fetch(`${API_BASE_URL}/superadmin/companies`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch companies');
    }
    
    return response.json();
  }

  async createCompanyAdmin(companyId: number, email: string, name: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/superadmin/companies/${companyId}/admin`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ email, name, role: 'admin' }),
    });
    if (!response.ok) {
      throw new Error('Failed to create admin');
    }
    return response.json();
  }

  // Admin endpoints
  async adminLogin(email: string): Promise<{ message: string; email: string }> {
    console.log(`🔍 Admin login request for: ${email}`);
    const response = await fetch(`${API_BASE_URL}/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, role: 'admin' }),
    });
    
    console.log(`📡 Admin login response status: ${response.status}`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('❌ Admin login error:', errorData);
      throw new Error(errorData.detail || 'Failed to send OTP');
    }
    
    const result = await response.json();
    console.log('✅ Admin login successful:', result);
    return result;
  }

  async adminVerifyOTP(email: string, otp: string): Promise<TokenResponse> {
    console.log(`🔍 Admin verify OTP request for: ${email}, OTP: ${otp}`);
    const response = await fetch(`${API_BASE_URL}/admin/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp, role: 'admin' }),
    });
    
    console.log(`📡 Admin verify OTP response status: ${response.status}`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('❌ Admin verify OTP error:', errorData);
      throw new Error(errorData.detail || 'Invalid OTP');
    }
    
    const result = await response.json();
    console.log('✅ Admin verify OTP successful:', result);
    return result;
  }

  async createUser(user: UserCreateRequest): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/admin/users`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(user),
    });
    
    if (!response.ok) {
      throw new Error('Failed to create user');
    }
    
    return response.json();
  }

  async getUsers(): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/admin/users`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    
    return response.json();
  }

  // User endpoints
  async userLogin(email: string): Promise<{ message: string; email: string }> {
    console.log(`🔍 User login request for: ${email}`);
    const response = await fetch(`${API_BASE_URL}/user/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, role: 'user' }),
    });
    
    console.log(`📡 User login response status: ${response.status}`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('❌ User login error:', errorData);
      throw new Error(errorData.detail || 'Failed to send OTP');
    }
    
    const result = await response.json();
    console.log('✅ User login successful:', result);
    return result;
  }

  async userVerifyOTP(email: string, otp: string): Promise<TokenResponse> {
    console.log(`🔍 User verify OTP request for: ${email}, OTP: ${otp}`);
    const response = await fetch(`${API_BASE_URL}/user/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp, role: 'user' }),
    });
    
    console.log(`📡 User verify OTP response status: ${response.status}`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('❌ User verify OTP error:', errorData);
      throw new Error(errorData.detail || 'Invalid OTP');
    }
    
    const result = await response.json();
    console.log('✅ User verify OTP successful:', result);
    return result;
  }

  async getUserProfile(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/user/profile`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch user profile');
    }
    
    return response.json();
  }

  // Appointment endpoints
  async createAppointment(appointment: AppointmentCreateRequest): Promise<Appointment> {
    const response = await fetch(`${API_BASE_URL}/appointments`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(appointment),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to create appointment');
    }
    
    return response.json();
  }

  async getAppointments(): Promise<Appointment[]> {
    const response = await fetch(`${API_BASE_URL}/appointments`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch appointments');
    }
    
    return response.json();
  }

  async getAppointment(appointmentId: number): Promise<Appointment> {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch appointment');
    }
    
    return response.json();
  }

  async updateAppointmentStatus(appointmentId: number, status: string): Promise<Appointment> {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/status`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ status }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to update appointment status');
    }
    
    return response.json();
  }

  async getVisitorAppointments(visitorEmail: string): Promise<Appointment[]> {
    const response = await fetch(`${API_BASE_URL}/appointments/visitor/${encodeURIComponent(visitorEmail)}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch visitor appointments');
    }
    
    return response.json();
  }

  // Employee endpoints
  async getEmployees(): Promise<Employee[]> {
    const response = await fetch(`${API_BASE_URL}/admin/employees`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch employees');
    }
    
    return response.json();
  }

  async getPublicEmployees(): Promise<Employee[]> {
    const response = await fetch(`${API_BASE_URL}/employees`, {
      headers: this.getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch employees');
    }
    
    return response.json();
  }

  async createEmployee(employee: EmployeeCreate): Promise<Employee> {
    const response = await fetch(`${API_BASE_URL}/admin/employees`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(employee),
    });
    
    if (!response.ok) {
      throw new Error('Failed to create employee');
    }
    
    return response.json();
  }

  async uploadEmployeesCSV(file: File): Promise<{ message: string; created_count: number; errors: string[] }> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/admin/employees/upload-csv`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Failed to upload employees CSV');
    }
    
    return response.json();
  }

  // Health check
  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  }
}

export const apiService = new ApiService(); 