import { createBrowserRouter, Navigate } from 'react-router-dom';
import { RequireAuth } from './RequireAuth';
import { AppLayout } from '../layout/AppLayout';
import { LoginPage } from '../pages/LoginPage';
import { StudentsPage } from '../pages/StudentsPage';
import { CreateStudentPage } from '../pages/CreateStudentPage';
import { PetSelectPage } from '../pages/PetSelectPage';
import { StudentDetailPage } from '../pages/StudentDetailPage';
import { PetHomePage } from '../pages/PetHomePage';
import { PointLogsPage } from '../pages/PointLogsPage';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    element: <RequireAuth />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { path: '/', element: <Navigate to='/students' replace /> },
          { path: '/students', element: <StudentsPage /> },
          { path: '/students/create', element: <CreateStudentPage /> },
          { path: '/students/:studentId/select-pet', element: <PetSelectPage /> },
          { path: '/students/:studentId', element: <StudentDetailPage /> },
          { path: '/students/:studentId/pet', element: <PetHomePage /> },
          { path: '/points', element: <PointLogsPage /> },
        ],
      },
    ],
  },
]);
