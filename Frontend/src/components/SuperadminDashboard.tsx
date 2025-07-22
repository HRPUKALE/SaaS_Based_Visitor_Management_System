import React, { useState, useEffect } from 'react';
import { apiService, Company } from '../services/api';
import { useAuth } from '../context/AuthContext';

const SuperadminDashboard: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newCompany, setNewCompany] = useState({ name: '', email: '' });
  const [creating, setCreating] = useState(false);
  const { logout } = useAuth();
  const [showAdminForm, setShowAdminForm] = useState(false);
  const [adminEmail, setAdminEmail] = useState('');
  const [adminName, setAdminName] = useState('');
  const [adminCompanyId, setAdminCompanyId] = useState<number | null>(null);
  const [adminCreating, setAdminCreating] = useState(false);
  const [adminError, setAdminError] = useState('');
  const [adminSuccess, setAdminSuccess] = useState('');


  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const data = await apiService.getCompanies();
      setCompanies(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch companies');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCompany = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setError('');

    try {
      const company = await apiService.createCompany(newCompany);
      setCompanies([company, ...companies]);
      setNewCompany({ name: '', email: '' });
      setShowCreateForm(false);
      // Prompt for admin details
      setAdminCompanyId(company.id);
      setShowAdminForm(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create company');
    } finally {
      setCreating(false);
    }
  };

  const handleCreateAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdminCreating(true);
    setAdminError('');
    setAdminSuccess('');
    try {
      if (!adminCompanyId) throw new Error('No company selected');
      await apiService.createCompanyAdmin(adminCompanyId, adminEmail, adminName);
      setAdminSuccess('Admin user created and invited!');
      setAdminEmail('');
      setAdminName('');
      setShowAdminForm(false);
    } catch (err: any) {
      setAdminError(err.message || 'Failed to create admin');
    } finally {
      setAdminCreating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Superadmin Dashboard
              </h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={logout}
                className="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Companies</h2>
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Add Company
            </button>
          </div>

          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {showCreateForm && (
            <div className="mb-6 bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Create New Company
              </h3>
              <form onSubmit={handleCreateCompany}>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                      Company Name
                    </label>
                    <input
                      type="text"
                      id="name"
                      required
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      value={newCompany.name}
                      onChange={(e) => setNewCompany({ ...newCompany, name: e.target.value })}
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                      Company Email
                    </label>
                    <input
                      type="email"
                      id="email"
                      required
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      value={newCompany.email}
                      onChange={(e) => setNewCompany({ ...newCompany, email: e.target.value })}
                    />
                  </div>
                </div>
                <div className="mt-6 flex space-x-3">
                  <button
                    type="submit"
                    disabled={creating}
                    className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {creating ? 'Creating...' : 'Create Company'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowCreateForm(false);
                      setNewCompany({ name: '', email: '' });
                      setError('');
                    }}
                    className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {showAdminForm && (
            <div className="mb-6 bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Create Admin for New Company
              </h3>
              {adminError && <div className="mb-2 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded">{adminError}</div>}
              {adminSuccess && <div className="mb-2 bg-green-50 border border-green-200 text-green-700 px-4 py-2 rounded">{adminSuccess}</div>}
              <form onSubmit={handleCreateAdmin}>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="adminEmail" className="block text-sm font-medium text-gray-700">
                      Admin Email
                    </label>
                    <input
                      type="email"
                      id="adminEmail"
                      required
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      value={adminEmail}
                      onChange={(e) => setAdminEmail(e.target.value)}
                    />
                  </div>
                  <div>
                    <label htmlFor="adminName" className="block text-sm font-medium text-gray-700">
                      Admin Name
                    </label>
                    <input
                      type="text"
                      id="adminName"
                      required
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      value={adminName}
                      onChange={(e) => setAdminName(e.target.value)}
                    />
                  </div>
                </div>
                <div className="mt-6 flex space-x-3">
                  <button
                    type="submit"
                    disabled={adminCreating}
                    className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {adminCreating ? 'Creating Admin...' : 'Create Admin'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowAdminForm(false)}
                    className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {companies.map((company) => (
                <li key={company.id}>
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                            <span className="text-indigo-600 font-medium">
                              {company.name.charAt(0).toUpperCase()}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {company.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {company.email}
                          </div>
                        </div>
                      </div>
                      <div className="text-sm text-gray-500">
                        Created: {new Date(company.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {companies.length === 0 && !loading && (
            <div className="text-center py-12">
              <p className="text-gray-500">No companies found. Create your first company above.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SuperadminDashboard; 