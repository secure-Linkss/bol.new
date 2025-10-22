import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { MapPin, Users, Globe, TrendingUp } from 'lucide-react';

const AtlasMap = () => {
  const [geoData, setGeoData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [totalVisitors, setTotalVisitors] = useState(0);

  useEffect(() => {
    fetchGeoData();
  }, []);

  const fetchGeoData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/analytics/geography');
      
      if (response.ok) {
        const data = await response.json();
        setGeoData(data.countries || []);
        setTotalVisitors(data.total_visitors || 0);
      }
    } catch (error) {
      console.error('Error fetching geography data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate region percentages
  const getRegionPercentage = (count) => {
    return totalVisitors > 0 ? ((count / totalVisitors) * 100).toFixed(1) : 0;
  };

  // Get color intensity based on visitor count
  const getColorIntensity = (count) => {
    if (count === 0) return 'bg-slate-700';
    const maxCount = Math.max(...geoData.map(d => d.visitors));
    const intensity = (count / maxCount) * 100;
    
    if (intensity > 75) return 'bg-blue-600';
    if (intensity > 50) return 'bg-blue-500';
    if (intensity > 25) return 'bg-blue-400';
    return 'bg-blue-300';
  };

  // Group data by continent/region
  const groupedData = geoData.reduce((acc, item) => {
    const region = item.continent || 'Other';
    if (!acc[region]) {
      acc[region] = [];
    }
    acc[region].push(item);
    return acc;
  }, {});

  if (loading) {
    return (
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Global Traffic Distribution</CardTitle>
          <CardDescription className="text-slate-400">Loading geography data...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-slate-800 border-slate-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-white flex items-center gap-2">
              <Globe className="h-5 w-5 text-blue-400" />
              Global Traffic Distribution
            </CardTitle>
            <CardDescription className="text-slate-400">
              Real-time visitor distribution across the world
            </CardDescription>
          </div>
          <Badge className="bg-blue-600 text-white">
            <Users className="h-3 w-3 mr-1" />
            {totalVisitors.toLocaleString()} Total Visitors
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <MapPin className="h-4 w-4 text-blue-400" />
              <span className="text-slate-400 text-xs">Countries</span>
            </div>
            <div className="text-2xl font-bold text-white">{geoData.length}</div>
          </div>
          
          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="h-4 w-4 text-green-400" />
              <span className="text-slate-400 text-xs">Top Country</span>
            </div>
            <div className="text-sm font-bold text-white truncate">
              {geoData[0]?.country_name || 'N/A'}
            </div>
          </div>
          
          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Users className="h-4 w-4 text-purple-400" />
              <span className="text-slate-400 text-xs">Top Visitors</span>
            </div>
            <div className="text-2xl font-bold text-white">
              {geoData[0]?.visitors || 0}
            </div>
          </div>
          
          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Globe className="h-4 w-4 text-cyan-400" />
              <span className="text-slate-400 text-xs">Continents</span>
            </div>
            <div className="text-2xl font-bold text-white">
              {Object.keys(groupedData).length}
            </div>
          </div>
        </div>

        {/* Regional Data */}
        <div className="space-y-6">
          {Object.entries(groupedData).map(([region, countries]) => {
            const regionTotal = countries.reduce((sum, c) => sum + c.visitors, 0);
            const regionPercentage = getRegionPercentage(regionTotal);
            
            return (
              <div key={region} className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                    <Globe className="h-4 w-4 text-blue-400" />
                    {region}
                  </h3>
                  <Badge className="bg-slate-700 text-slate-300">
                    {regionTotal.toLocaleString()} visitors ({regionPercentage}%)
                  </Badge>
                </div>

                {/* Countries in Region */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {countries.sort((a, b) => b.visitors - a.visitors).map((country, index) => (
                    <div
                      key={country.country_code || index}
                      className={`${getColorIntensity(country.visitors)} bg-opacity-20 border border-slate-600 rounded-lg p-4 hover:scale-105 transition-transform cursor-pointer`}
                      onClick={() => setSelectedRegion(country)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="text-2xl">{country.flag || '🌍'}</span>
                          <span className="font-semibold text-white text-sm truncate">
                            {country.country_name || country.country || 'Unknown'}
                          </span>
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-400">Visitors</span>
                          <span className="text-sm font-bold text-white">
                            {country.visitors.toLocaleString()}
                          </span>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-400">Percentage</span>
                          <span className="text-sm font-semibold text-blue-400">
                            {getRegionPercentage(country.visitors)}%
                          </span>
                        </div>
                        
                        {country.clicks && (
                          <div className="flex justify-between items-center">
                            <span className="text-xs text-slate-400">Clicks</span>
                            <span className="text-sm font-semibold text-green-400">
                              {country.clicks.toLocaleString()}
                            </span>
                          </div>
                        )}
                      </div>
                      
                      {/* Progress bar */}
                      <div className="mt-3 bg-slate-700 rounded-full h-1.5">
                        <div 
                          className="bg-blue-500 h-full rounded-full transition-all duration-300"
                          style={{ width: `${getRegionPercentage(country.visitors)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* No Data State */}
        {geoData.length === 0 && (
          <div className="text-center py-12">
            <Globe className="h-16 w-16 text-slate-600 mx-auto mb-4" />
            <p className="text-slate-400 text-lg">No geographic data available yet</p>
            <p className="text-slate-500 text-sm mt-2">
              Start tracking links to see visitor distribution
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AtlasMap;
