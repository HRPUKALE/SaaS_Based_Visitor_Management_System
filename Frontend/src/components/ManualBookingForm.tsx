import React, { useState, useEffect } from 'react';
import Logo from './Logo';
import { AppointmentBooking } from '../types';
import { apiService, AppointmentCreateRequest, Employee } from '../services/api';

interface ManualBookingFormProps {
  onBook: (data: AppointmentBooking) => void;
  onBack: () => void;
}

function convertTo24Hour(timeStr: string): string {
  const [time, modifier] = timeStr.toLowerCase().split(' ');
  let [hours, minutes] = time.split(':');
  let hoursNum = parseInt(hours, 10);
  if (modifier === 'pm' && hoursNum !== 12) hoursNum += 12;
  if (modifier === 'am' && hoursNum === 12) hoursNum = 0;
  return `${hoursNum.toString().padStart(2, '0')}:${minutes}`;
}

function isValidFutureAppointment(dateStr: string, timeStr: string): boolean {
  const time24 = convertTo24Hour(timeStr); // Normalize first
  const appointmentDateTime = new Date(`${dateStr}T${time24}`);
  const now = new Date();
  return appointmentDateTime > now;
}

const ManualBookingForm: React.FC<ManualBookingFormProps> = ({ onBook, onBack }) => {
  const today = new Date().toISOString().split('T')[0];
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [department, setDepartment] = useState('');
  const [employee, setEmployee] = useState('');
  const [reason, setReason] = useState('');
  const [time, setTime] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch employees on component mount
  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const data = await apiService.getPublicEmployees();
        setEmployees(data);
      } catch (err) {
        console.error('Error fetching employees:', err);
        setError('Failed to load employees. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  // Extract unique departments from employees data
  const departmentList = Array.from(new Set(employees.map(e => e.department)));

  // Filter employees by selected department
  const availableEmployees = department
    ? employees.filter(e => e.department === department)
    : [];

  // Compute if selected time is in the past (for today)
  const now = new Date();
  let timeInPast = false;
  if (time) {
    const [selectedHour, selectedMinute] = time.split(":").map(Number);
    const selectedDate = new Date();
    selectedDate.setHours(selectedHour, selectedMinute, 0, 0);
    if (today === now.toISOString().split('T')[0] && selectedDate < now) {
      timeInPast = true;
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      // Validate time if booking for today
      const now = new Date();
      const [selectedHour, selectedMinute] = time.split(":").map(Number);
      const selectedDate = new Date();
      selectedDate.setHours(selectedHour, selectedMinute, 0, 0);
      if (today === now.toISOString().split('T')[0] && selectedDate < now) {
        setError("You cannot book an appointment for a time that has already passed today.");
        return;
      }

      if (!isValidFutureAppointment(today, time)) {
        setError("Sorry, the time you selected has already passed. Please choose a future time.");
        return;
      }

      // Create appointment using API
      const appointmentData: AppointmentCreateRequest = {
        employee_name: employee,
        department,
        reason: reason || undefined,
        appointment_date: today,
        appointment_time: time,
        visitor_name: fullName,
        visitor_email: email,
        visitor_phone: phone || undefined,
        booking_method: 'manual'
      };

      const createdAppointment = await apiService.createAppointment(appointmentData);

      // Call the original onBook callback with the created appointment data
      const booking: AppointmentBooking = {
        employee_name: employee,
        department,
        reason,
        appointment_time: time,
        visitor_name: fullName,
        email,
        phone,
        appointment_date: today,
      };

      onBook(booking);
      setTime(''); // Reset time after booking

    } catch (err) {
      console.error('Error creating appointment:', err);
      setError(err instanceof Error ? err.message : 'Failed to create appointment. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50 py-8 px-2">
        <Logo className="mb-6" />
        <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-lg md:max-w-md sm:max-w-full">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-lg">Loading employees...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50 py-8 px-2">
      <Logo className="mb-6" />
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-lg md:max-w-md sm:max-w-full">
        <h2 className="text-2xl font-bold mb-4">Appointment Details</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="text-red-600 font-semibold text-center">{error}</div>
          )}
          <div>
            <label className="block font-medium mb-1">Department *</label>
            <select
              className="w-full border rounded px-3 py-2"
              value={department}
              onChange={(e) => {
                setDepartment(e.target.value);
                setEmployee('');
              }}
              required
            >
              <option value="">Select a department</option>
              {departmentList.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block font-medium mb-1">Employee *</label>
            <select
              className="w-full border rounded px-3 py-2"
              value={employee}
              onChange={(e) => setEmployee(e.target.value)}
              required
              disabled={!department}
            >
              <option value="">Select department first</option>
              {availableEmployees.map((emp) => (
                <option key={emp.name} value={emp.name}>{emp.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block font-medium mb-1">Reason for Visit</label>
            <textarea
              className="w-full border rounded px-3 py-2"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="Brief description of your visit purpose..."
            />
          </div>
          {/* Date is hidden, set to today */}
          <input type="hidden" value={today} readOnly />
          <div>
            <label className="block font-medium mb-1">Time *</label>
            <select
              className="w-full border rounded px-3 py-2"
              value={time}
              onChange={(e) => setTime(e.target.value)}
              required
            >
              <option value="">Select a time slot</option>
              <option value="09:00">09:00 AM</option>
              <option value="10:00">10:00 AM</option>
              <option value="11:00">11:00 AM</option>
              <option value="12:00">12:00 PM</option>
              <option value="14:00">02:00 PM</option>
              <option value="15:00">03:00 PM</option>
              <option value="16:00">04:00 PM</option>
            </select>
            {timeInPast && (
              <div className="text-red-600 font-semibold mt-1">You cannot select a time that has already passed today.</div>
            )}
          </div>
          <div>
            <label className="block font-medium mb-1">Full Name *</label>
            <input
              className="w-full border rounded px-3 py-2"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              placeholder="Enter your full name"
            />
          </div>
          <div>
            <label className="block font-medium mb-1">Email Address *</label>
            <input
              className="w-full border rounded px-3 py-2"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email address"
            />
          </div>
          <div>
            <label className="block font-medium mb-1">Phone Number *</label>
            <input
              className="w-full border rounded px-3 py-2"
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
              placeholder="Enter your phone number"
            />
          </div>
          <div className="flex gap-4 mt-6">
            <button
              type="button"
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded"
              onClick={onBack}
            >
              Back
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              disabled={timeInPast || isSubmitting}
            >
              {isSubmitting ? 'Booking...' : 'Book Appointment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ManualBookingForm; 