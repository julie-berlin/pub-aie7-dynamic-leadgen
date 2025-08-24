import { useState, useEffect } from 'react';
import { useAdminStore } from '../stores/adminStore';
import { API_ENDPOINTS } from '../config/api';
import LogoUpload from '../components/LogoUpload';

interface CompanySettings {
  name: string;
  businessObjective: string;
  industry: string;
  description: string;
  website?: string;
  phone?: string;
  address?: string;
  logoUrl?: string;
}

export default function SettingsPage() {
  const { user } = useAdminStore();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [settings, setSettings] = useState<CompanySettings>({
    name: '',
    businessObjective: '',
    industry: '',
    description: '',
    website: '',
    phone: '',
    address: '',
    logoUrl: ''
  });
  const [originalSettings, setOriginalSettings] = useState<CompanySettings | null>(null);

  const hasChanges = originalSettings ? JSON.stringify(settings) !== JSON.stringify(originalSettings) : false;

  useEffect(() => {
    // Auth is guaranteed to be ready when this component renders
    loadSettings();
  }, []);

  const loadSettings = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        console.error('No admin token found');
        return;
      }

      const response = await fetch(API_ENDPOINTS.CLIENTS.ME, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        }
      });

      if (response.ok) {
        const { data } = await response.json();
        const clientSettings = {
          name: data.business_name || data.name || '',
          businessObjective: data.goals || '',
          industry: data.industry || '',
          description: data.background || '',
          website: data.website || '',
          phone: data.phone || '',
          address: data.address || '',
          logoUrl: data.logo_url || ''
        };
        setSettings(clientSettings);
        setOriginalSettings(clientSettings);
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        console.error('No admin token found');
        return;
      }

      const response = await fetch(API_ENDPOINTS.CLIENTS.ME, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          business_name: settings.name,
          goals: settings.businessObjective,
          industry: settings.industry,
          background: settings.description,
          website: settings.website,
          phone: settings.phone,
          address: settings.address,
          logo_url: settings.logoUrl
        })
      });

      if (response.ok) {
        const { data } = await response.json();
        const updatedSettings = {
          name: data.business_name || data.name || '',
          businessObjective: data.goals || '',
          industry: data.industry || '',
          description: data.background || '',
          website: data.website || '',
          phone: data.phone || '',
          address: data.address || '',
          logoUrl: data.logo_url || ''
        };
        setOriginalSettings(updatedSettings);
        setSettings(updatedSettings);
      } else {
        throw new Error('Failed to save settings');
      }
    } catch (error) {
      console.error('Failed to save settings:', error);
      alert('Failed to save settings. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const resetSettings = () => {
    if (originalSettings) {
      setSettings({ ...originalSettings });
    }
  };

  const handleLogoChange = (logoUrl: string | null) => {
    setSettings(prev => ({ ...prev, logoUrl: logoUrl || '' }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading settings...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Company Settings</h1>
          <p className="text-slate-600 mt-1">Manage your business information and preferences</p>
        </div>
      </div>

      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="text-lg font-medium text-slate-900">Business Information</h3>
          <p className="text-sm text-slate-500">This information is used by AI agents to personalize surveys and responses.</p>
        </div>
        
        <div className="admin-card-body space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="admin-form-group">
              <label htmlFor="company-name" className="admin-label">
                Company Name *
              </label>
              <input
                type="text"
                id="company-name"
                value={settings.name}
                onChange={(e) => setSettings(prev => ({ ...prev, name: e.target.value }))}
                className="admin-input"
                placeholder="Your Company Name"
                required
              />
            </div>

            <div className="admin-form-group">
              <label htmlFor="industry" className="admin-label">
                Industry
              </label>
              <input
                type="text"
                id="industry"
                value={settings.industry}
                onChange={(e) => setSettings(prev => ({ ...prev, industry: e.target.value }))}
                className="admin-input"
                placeholder="e.g., Technology, Healthcare, Retail"
              />
            </div>

            <div className="admin-form-group lg:col-span-2">
              <label htmlFor="business-objective" className="admin-label">
                Business Objective *
              </label>
              <textarea
                id="business-objective"
                rows={3}
                value={settings.businessObjective}
                onChange={(e) => setSettings(prev => ({ ...prev, businessObjective: e.target.value }))}
                className="admin-input"
                placeholder="Describe your main business goals and objectives..."
                required
              />
              <p className="admin-help-text">
                Help AI understand your business goals to create more targeted surveys.
              </p>
            </div>

            <div className="admin-form-group lg:col-span-2">
              <label htmlFor="description" className="admin-label">
                Company Description
              </label>
              <textarea
                id="description"
                rows={4}
                value={settings.description}
                onChange={(e) => setSettings(prev => ({ ...prev, description: e.target.value }))}
                className="admin-input"
                placeholder="Tell us more about your company, products, and services..."
              />
            </div>

            <div className="admin-form-group">
              <label htmlFor="website" className="admin-label">
                Website
              </label>
              <input
                type="url"
                id="website"
                value={settings.website}
                onChange={(e) => setSettings(prev => ({ ...prev, website: e.target.value }))}
                className="admin-input"
                placeholder="https://yourcompany.com"
              />
            </div>

            <div className="admin-form-group">
              <label htmlFor="phone" className="admin-label">
                Phone Number
              </label>
              <input
                type="tel"
                id="phone"
                value={settings.phone}
                onChange={(e) => setSettings(prev => ({ ...prev, phone: e.target.value }))}
                className="admin-input"
                placeholder="(555) 123-4567"
              />
            </div>

            <div className="admin-form-group lg:col-span-2">
              <label htmlFor="address" className="admin-label">
                Address
              </label>
              <input
                type="text"
                id="address"
                value={settings.address}
                onChange={(e) => setSettings(prev => ({ ...prev, address: e.target.value }))}
                className="admin-input"
                placeholder="123 Main St, City, State 12345"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-6 border-t border-slate-200">
            <div className="text-sm text-slate-500">
              {hasChanges && 'You have unsaved changes'}
            </div>
            <div className="flex space-x-3">
              <button
                type="button"
                onClick={resetSettings}
                disabled={!hasChanges || saving}
                className="admin-btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Reset
              </button>
              <button
                type="button"
                onClick={saveSettings}
                disabled={!hasChanges || saving || !settings.name || !settings.businessObjective}
                className="admin-btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="text-lg font-medium text-slate-900">Brand Assets</h3>
          <p className="text-sm text-slate-500">Upload your company logo to personalize your forms and surveys.</p>
        </div>
        
        <div className="admin-card-body">
          <LogoUpload
            currentLogoUrl={settings.logoUrl}
            onLogoChange={handleLogoChange}
            disabled={saving}
          />
        </div>
      </div>

      <div className="admin-card">
        <div className="admin-card-header">
          <h3 className="text-lg font-medium text-slate-900">Account Information</h3>
          <p className="text-sm text-slate-500">Your admin account details</p>
        </div>
        
        <div className="admin-card-body">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <label className="admin-label">Admin Name</label>
              <div className="mt-1 text-sm text-slate-900">{user?.name || 'Not provided'}</div>
            </div>
            <div>
              <label className="admin-label">Email</label>
              <div className="mt-1 text-sm text-slate-900">{user?.email || 'Not provided'}</div>
            </div>
            <div>
              <label className="admin-label">Role</label>
              <div className="mt-1">
                <span className="admin-badge admin-badge-info">Administrator</span>
              </div>
            </div>
            <div>
              <label className="admin-label">Client ID</label>
              <div className="mt-1 text-sm text-slate-500 font-mono">{user?.clientId || 'Not available'}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}