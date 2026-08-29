export type Employee = {
  id: number;
  name: string;
  username: string;
  is_admin: boolean;
  is_active: boolean;
};

export type ServiceType = {
  id: number;
  name: string;
  is_active: boolean;
};

export type ServiceReportItem = {
  service_type_id: number;
  name: string;
  total: number;
};

export type ServiceOrderReport = {
  total_service_orders: number;
  services: ServiceReportItem[];
};

export type MonthlyReport = {
  month: number;
  total_service_orders: number;
  services: ServiceReportItem[];
};

export type ServiceOrder = {
  id: number;
  plate: string;
  employee_id: number;
  employee?: Pick<Employee, "id" | "name">;
  created_at: string;
  updated_at?: string;
};