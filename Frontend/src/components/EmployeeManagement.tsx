import React, { useState, useEffect } from 'react';
import { apiService, Employee, EmployeeCreate } from '../services/api';

interface EmployeeManagementProps {
  onBack: () => void;
}

const EmployeeManagement: React.FC<EmployeeManagementProps> = ({ onBack }) => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<'list' | 'manual' | 'csv'>('list');
  const [newEmployee, setNewEmployee] = useState<EmployeeCreate>({
    name: '',
    email: '',
    department: '',
    designation: '',
    phone: ''
  });
  const [creating, setCreating] = useState(false);
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ message: string; created_count: number; errors: string[] } | null>(null);

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      const data = await apiService.getEmployees();
      setEmployees(data);
    } catch (err) {
      console.error('Error loading employees:', err);
      setError(err instanceof Error ? err.message : 'Failed to load employees');
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setError('');

    try {
      const employee = await apiService.createEmployee(newEmployee);
      setEmployees([employee, ...employees]);
      setNewEmployee({ name: '', email: '', department: '', designation: '', phone: '' });
      setCurrentView('list');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create employee');
    } finally {
      setCreating(false);
    }
  };

  const handleCsvUpload = async () => {
    if (!csvFile) {
      setError('Please select a CSV file');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const result = await apiService.uploadEmployeesCSV(csvFile);
      setUploadResult(result);
      if (result.created_count > 0) {
        await loadEmployees(); // Refresh the list
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload CSV');
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'text/csv') {
      setCsvFile(file);
      setError('');
    } else {
      setError('Please select a valid CSV file');
      setCsvFile(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50">
        <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-6xl">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-lg">Loading employees...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-blue-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Employee Management</h1>
              <p className="text-gray-600 mt-1">
                Manage company employees and departments for appointment booking
              </p>
            </div>
            <div className="flex gap-4">
              <button
                onClick={loadEmployees}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Refresh
              </button>
              <button
                onClick={onBack}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
              >
                Back
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex space-x-8 border-b">
            <button
              onClick={() => setCurrentView('list')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                currentView === 'list'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Employee List
            </button>
            <button
              onClick={() => setCurrentView('manual')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                currentView === 'manual'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Manual Entry
            </button>
            <button
              onClick={() => setCurrentView('csv')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                currentView === 'csv'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              CSV Upload
            </button>
          </div>
        </div>

        {/* Content */}
        {currentView === 'list' && (
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            {employees.length === 0 ? (
              <div className="p-8 text-center">
                <p className="text-gray-500 text-lg">No employees found.</p>
                <button
                  onClick={() => setCurrentView('manual')}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Add First Employee
                </button>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Employee
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Department
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Designation
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Contact
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {employees.map((employee) => (
                      <tr key={employee.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900">
                              {employee.name}
                            </div>
                            <div className="text-sm text-gray-500">
                              {employee.email}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {employee.department}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {employee.designation || '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {employee.phone || '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            employee.is_active 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {employee.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {currentView === 'manual' && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-6">Add Employee Manually</h2>
            
            {error && (
              <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <form onSubmit={handleManualSubmit} className="space-y-6">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={newEmployee.name}
                    onChange={(e) => setNewEmployee({ ...newEmployee, name: e.target.value })}
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={newEmployee.email}
                    onChange={(e) => setNewEmployee({ ...newEmployee, email: e.target.value })}
                  />
                </div>
                <div>
                  <label htmlFor="department" className="block text-sm font-medium text-gray-700">
                    Department *
                  </label>
                  <input
                    type="text"
                    id="department"
                    required
                    placeholder="e.g., HR, IT, Sales"
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={newEmployee.department}
                    onChange={(e) => setNewEmployee({ ...newEmployee, department: e.target.value })}
                  />
                </div>
                <div>
                  <label htmlFor="designation" className="block text-sm font-medium text-gray-700">
                    Designation
                  </label>
                  <input
                    type="text"
                    id="designation"
                    placeholder="e.g., Manager, Developer, Analyst"
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={newEmployee.designation}
                    onChange={(e) => setNewEmployee({ ...newEmployee, designation: e.target.value })}
                  />
                </div>
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    placeholder="e.g., +1234567890"
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={newEmployee.phone}
                    onChange={(e) => setNewEmployee({ ...newEmployee, phone: e.target.value })}
                  />
                </div>
              </div>
              
              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={creating}
                  className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                >
                  {creating ? 'Creating...' : 'Add Employee'}
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentView('list')}
                  className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {currentView === 'csv' && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-6">Upload Employees via CSV</h2>
            
            {error && (
              <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {uploadResult && (
              <div className={`mb-4 border px-4 py-3 rounded ${
                uploadResult.errors.length > 0 
                  ? 'bg-yellow-50 border-yellow-200 text-yellow-700'
                  : 'bg-green-50 border-green-200 text-green-700'
              }`}>
                <div className="font-medium">{uploadResult.message}</div>
                {uploadResult.errors.length > 0 && (
                  <div className="mt-2">
                    <div className="font-medium">Errors:</div>
                    <ul className="list-disc list-inside mt-1">
                      {uploadResult.errors.map((error, index) => (
                        <li key={index} className="text-sm">{error}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <div className="space-y-6">
              <div>
                <label htmlFor="csv-file" className="block text-sm font-medium text-gray-700 mb-2">
                  Select CSV File
                </label>
                <input
                  type="file"
                  id="csv-file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                <p className="mt-2 text-sm text-gray-500">
                  CSV should have columns: name, email, department, designation (optional), phone (optional)
                </p>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-medium text-gray-900 mb-2">CSV Template:</h3>
                <pre className="text-sm text-gray-600">
{`name,email,department,designation,phone
John Doe,john@company.com,IT,Developer,+1234567890
Jane Smith,jane@company.com,HR,Manager,+1234567891
Bob Johnson,bob@company.com,Sales,Representative,+1234567892`}
                </pre>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleCsvUpload}
                  disabled={!csvFile || uploading}
                  className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                >
                  {uploading ? 'Uploading...' : 'Upload CSV'}
                </button>
                <button
                  onClick={() => setCurrentView('list')}
                  className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmployeeManagement; 