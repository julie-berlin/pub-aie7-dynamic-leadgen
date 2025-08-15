import { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

interface BusinessInfo {
  name: string;
  industry?: string;
}

export function useBusinessInfo() {
  const [businessInfo, setBusinessInfo] = useState<BusinessInfo>({ name: 'Survey Admin' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadBusinessInfo = async () => {
      try {
        const response = await fetch(API_ENDPOINTS.CLIENTS.ME, {
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (response.ok) {
          const { data } = await response.json();
          setBusinessInfo({
            name: data.business_name || data.name || 'Survey Admin',
            industry: data.industry
          });
        }
      } catch (error) {
        console.error('Failed to load business info:', error);
        // Keep default name on error
      } finally {
        setLoading(false);
      }
    };

    loadBusinessInfo();
  }, []);

  return { businessInfo, loading };
}