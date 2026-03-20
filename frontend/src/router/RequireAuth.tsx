import { Navigate, Outlet } from 'react-router-dom';

export function RequireAuth() {
  const token = localStorage.getItem('class_pets_token');
  if (!token) {
    return <Navigate to='/login' replace />;
  }
  return <Outlet />;
}
