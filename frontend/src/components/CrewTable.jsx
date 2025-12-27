//availibility undo feature remaining
export default function CrewTable({ crew }) {
  const statusColors = {
    'Available': 'bg-green-500',
    'Assigned': 'bg-blue-500',
    'On Duty': 'bg-blue-600',
    'Fatigued': 'bg-red-500',
    'On Leave': 'bg-gray-500',
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Base</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hours (7d/30d)</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Performance</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reliability</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Experience</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {crew.map((member) => (
              <tr key={member.emp_id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold">
                      {getInitials(member.name)}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">{member.name}</p>
                      <p className="text-sm text-gray-500">{member.emp_id}</p>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-700">{member.designation}</td>
                <td className="px-6 py-4 font-semibold">{member.baseLocation}</td>
                <td className="px-6 py-4">
                  <span>{member.hoursWorked7d || 0}h / {member.hoursWorked30d || 0}h</span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-green-500"
                        style={{ width: `${member.performanceScore}%` }}
                      />
                    </div>
                    <span className="font-semibold">{member.performanceScore / 20}/5</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-green-600 font-semibold">
                  {member.reliabilityScore}%
                </td>
                <td className="px-6 py-4">
                  <div>
                    <p className="font-semibold">{member.yearsExperience || 0} yrs</p>
                    <p className="text-sm text-gray-500">{member.totalFlightHours || 0}h</p>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium text-white ${statusColors[member.availability] || 'bg-gray-500'}`}>
                    {member.availability}
                  </span>
                  {member.assignedFlight && (
                    <p className="text-xs text-gray-500 mt-1">Flight: {member.assignedFlight}</p>
                  )}
                </td>
                <td className="px-6 py-4">
                  <button className="text-blue-600 hover:text-blue-800 font-medium">
                    👁 Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
