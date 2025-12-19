import { Plane } from 'lucide-react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-gradient-to-r from-blue-700 to-blue-500 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-white p-2 rounded-lg">
              <Plane className="w-8 h-8 text-blue-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">CrewSync</h1>
              <p className="text-sm text-blue-100">17-Parameter Data Structures-Driven Crew Management</p>
            </div>
          </div>
        </div>
        
        <div className="flex gap-4 mt-4">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-white text-blue-600 font-semibold'
                  : 'text-white hover:bg-blue-600'
              }`
            }
          >
             Dashboard
          </NavLink>
          <NavLink
            to="/crew"
            className={({ isActive }) =>
              `px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-white text-blue-600 font-semibold'
                  : 'text-white hover:bg-blue-600'
              }`
            }
          >
             Crew Management
          </NavLink>
          <NavLink
            to="/recommendations"
            className={({ isActive }) =>
              `px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-white text-blue-600 font-semibold'
                  : 'text-white hover:bg-blue-600'
              }`
            }
          >
             Recommendations
          </NavLink>
        </div>
      </div>
    </nav>
  );
}
