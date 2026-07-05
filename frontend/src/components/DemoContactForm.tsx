import React, { useState } from 'react';

export const DemoContactForm = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [address, setAddress] = useState({ village: '', subDistrict: '', district: '', state: '' });

  const handleSearch = async (val: string) => {
    setQuery(val);
    if (val.length >= 2) {
      // Direct call targeting the 6.5 format specification payload
      const res = await fetch(`http://localhost:3000/v1/autocomplete?q=${val}`);
      const json = await res.json();
      if (json.success) setSuggestions(json.data);
    }
  };

  const selectVillage = (item: any) => {
    setAddress({
      village: item.hierarchy.village,
      subDistrict: item.hierarchy.subDistrict,
      district: item.hierarchy.district,
      state: item.hierarchy.state
    });
    setSuggestions([]);
    setQuery(item.label);
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4 border border-gray-200">
      <h2 className="text-xl font-bold text-gray-800">B2B Integration Demo Form</h2>
      <div>
        <label className="block text-sm font-medium text-gray-700">Village/Area Autocomplete</label>
        <input 
          type="text" value={query} onChange={(e) => handleSearch(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
          placeholder="Start typing (e.g., Manibeli)..."
        />
        {suggestions.length > 0 && (
          <ul className="border bg-white position-absolute w-full z-10 max-h-40 overflow-y-auto">
            {suggestions.map((item: any) => (
              <li key={item.value} onClick={() => selectVillage(item)} className="p-2 hover:bg-gray-100 cursor-pointer text-sm">
                {item.fullAddress}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
        <div><strong>Sub-District:</strong> <p className="p-2 bg-gray-50 rounded">{address.subDistrict || '-'}</p></div>
        <div><strong>District:</strong> <p className="p-2 bg-gray-50 rounded">{address.district || '-'}</p></div>
        <div className="col-span-2"><strong>State:</strong> <p className="p-2 bg-gray-50 rounded">{address.state || '-'}</p></div>
      </div>
    </div>
  );
};
