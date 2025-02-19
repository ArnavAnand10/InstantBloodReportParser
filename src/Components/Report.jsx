import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Report() {
  const navigate = useNavigate();
  
  // Hardcoded blood report data
  const hardcodedReport = {
    id: 1,
    date: '02/19/2025',
    hemoglobin: '14.2',
    wbcCount: '7.3',
    rbcCount: '5.1',
    platelets: '220',
    hematocrit: '42.5',
    glucose: '92',
    cholesterol: '185',
  };

  // Reference ranges for common blood parameters
  const referenceRanges = {
    hemoglobin: { min: 12, max: 16, unit: 'g/dL' },
    wbcCount: { min: 4.5, max: 11, unit: 'x10³/μL' },
    rbcCount: { min: 4.2, max: 5.8, unit: 'x10⁶/μL' },
    platelets: { min: 150, max: 450, unit: 'x10³/μL' },
    hematocrit: { min: 36, max: 48, unit: '%' },
    glucose: { min: 70, max: 100, unit: 'mg/dL' },
    cholesterol: { min: 0, max: 200, unit: 'mg/dL' },
  };

  // Function to determine if a value is within normal range
  const getStatus = (param, value) => {
    const numValue = parseFloat(value);
    if (isNaN(numValue)) return 'neutral';
    
    const range = referenceRanges[param];
    if (numValue < range.min) return 'low';
    if (numValue > range.max) return 'high';
    return 'normal';
  };

  // Function to get status badge class
  const getStatusBadge = (status) => {
    switch (status) {
      case 'low': return 'badge badge-warning';
      case 'high': return 'badge badge-error';
      case 'normal': return 'badge badge-success';
      default: return 'badge';
    }
  };

  // Function to get readable parameter name
  const getReadableName = (param) => {
    const nameMap = {
      hemoglobin: 'Hemoglobin',
      wbcCount: 'WBC Count',
      rbcCount: 'RBC Count',
      platelets: 'Platelets',
      hematocrit: 'Hematocrit',
      glucose: 'Glucose',
      cholesterol: 'Cholesterol',
    };
    return nameMap[param] || param;
  };

  // Handle button click to redirect to UploadFiles component
  const handleAddNewReport = () => {
    navigate('/');
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-primary">Blood Report Summary</h1>
        <button 
          className="btn btn-primary" 
          onClick={handleAddNewReport}
        >
          Add New Report
        </button>
      </div>

      <div className="card bg-base-100 shadow-xl mb-6">
        <div className="card-body">
          <h2 className="card-title flex justify-between">
            <span>Blood Report</span>
            <span className="text-sm opacity-70">{hardcodedReport.date}</span>
          </h2>
          
          <div className="overflow-x-auto">
            <table className="table table-zebra w-full">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Value</th>
                  <th>Reference Range</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.keys(hardcodedReport)
                  .filter(key => key !== 'id' && key !== 'date')
                  .map((param) => {
                    if (!hardcodedReport[param]) return null;
                    
                    const status = getStatus(param, hardcodedReport[param]);
                    const range = referenceRanges[param];
                    
                    return (
                      <tr key={param}>
                        <td>{getReadableName(param)}</td>
                        <td>{hardcodedReport[param]} {range.unit}</td>
                        <td>
                          {range.min} - {range.max} {range.unit}
                        </td>
                        <td>
                          <span className={getStatusBadge(status)}>
                            {status === 'low' ? 'Low' : 
                             status === 'high' ? 'High' : 
                             status === 'normal' ? 'Normal' : 'N/A'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </div>
          
          <div className="mt-6">
            <h3 className="font-bold text-lg">Summary Analysis</h3>
            <p className="py-2">All blood parameters are within normal ranges. Continue with regular health monitoring and maintain current lifestyle habits.</p>
          </div>
        </div>
      </div>
    </div>
  );
}