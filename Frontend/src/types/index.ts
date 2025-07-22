export interface AppointmentState {
  employee_name: string | null;
  department: string | null;
  reason: string | null;
  appointment_time: string | null;
  visitor_name: string | null;
  email: string | null;
  phone: string | null;
  appointment_date: string;
}

export interface Employee {
  employee_name: string;
  department: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface AppointmentBooking {
  employee_name: string;
  department: string;
  reason: string;
  appointment_time: string;
  visitor_name: string;
  email: string;
  phone: string;
  appointment_date: string;
}