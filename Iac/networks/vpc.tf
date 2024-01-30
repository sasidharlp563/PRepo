
resource "aws_vpc" "main" {
  cidr_block       = var.primary_vpc_cidr
  instance_tenancy = "default"
  enable_dns_hostnames = true
  enable_dns_support = true
  tags = {
    Name = "VPC"
    project=var.project_name
  }
}
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc_ipv4_cidr_block_association" "secondary_vpc_cidr" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.secondary_vpc_cidr
}

resource "aws_subnet" "kube-public-subnet-1" {
  vpc_id     = aws_vpc_ipv4_cidr_block_association.secondary_vpc_cidr.vpc_id
  cidr_block = "10.82.0.0/21"
  map_public_ip_on_launch = true
  availability_zone = data.aws_availability_zones.available.names[0]
  tags = {
    Name = "web-public-subnet-1"
    project=var.project_name
  }
}

resource "aws_internet_gateway" "vpc_internet_gateway" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "internet-gateway"
    project=var.project_name
  }
}
resource "aws_route_table" "kube-public-subnets-route-table" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpc_internet_gateway.id

  }
  tags = {
    Name = "kube-public-subnets-route-table"
    project=var.project_name
  }
}

resource "aws_subnet" "kube-private-subnet-1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.81.0.0/18"
  availability_zone = data.aws_availability_zones.available.names[0]
  tags = {
    Name = "kube-private-subnet-1"
    project=var.project_name
  }
}

resource "aws_subnet" "kube-private-subnet-2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.81.64.0/18"
  availability_zone = data.aws_availability_zones.available.names[1]
  tags = {
    Name = "kube-private-subnet-2"
    project=var.project_name
  }
}

resource "aws_subnet" "kube-private-subnet-3" {
  vpc_id     = aws_vpc.main.id
  cidr_block = 	"10.81.128.0/18"
  availability_zone = data.aws_availability_zones.available.names[2]
  tags = {
    Name = "kube-private-subnet-3"
    project=var.project_name
  }
}

resource "aws_route_table" "kube-subnets-route-table" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "kube-subnets-route-table"
    project=var.project_name

  }
}





resource "aws_eip" "nat-gateway-ip-1" {
  vpc      = true
  tags = {
    Name = "nat-gateway-ip-1"
    project=var.project_name
  }
}


resource "aws_nat_gateway" "natgateway-1" {
  allocation_id = aws_eip.nat-gateway-ip-1.id
  subnet_id     = aws_subnet.kube-public-subnet-1.id

  tags = {
    Name = "natgateway-1"
    project=var.project_name
  }
  depends_on = [aws_internet_gateway.vpc_internet_gateway]
}


resource "aws_route" "kube-subnets-to-internet-route" {
  route_table_id            = aws_route_table.kube-subnets-route-table.id
  destination_cidr_block    = "0.0.0.0/0"
  nat_gateway_id = aws_nat_gateway.natgateway-1.id
  depends_on                = [
    aws_route_table.kube-subnets-route-table,
    aws_nat_gateway.natgateway-1
  ]
}



resource "aws_route_table_association" "kube-public-subnet-1-rtb-association" {
  subnet_id      = aws_subnet.kube-public-subnet-1.id
  route_table_id = aws_route_table.kube-subnets-route-table.id
}

resource "aws_route_table_association" "kube-private-subnet-1-rtb-association" {
  subnet_id      = aws_subnet.kube-private-subnet-1.id
  route_table_id = aws_route_table.kube-subnets-route-table.id
}

resource "aws_route_table_association" "kube-private-subnet-2-rtb-association" {
  subnet_id      = aws_subnet.kube-private-subnet-2.id
  route_table_id = aws_route_table.kube-subnets-route-table.id
}

resource "aws_route_table_association" "kube-private-subnet-3-rtb-association" {
  subnet_id      = aws_subnet.kube-private-subnet-3.id
  route_table_id = aws_route_table.kube-subnets-route-table.id
}


output "subnet-1" {
  value = aws_subnet.kube-private-subnet-1.id
}

output "subnet-2" {
  value = aws_subnet.kube-private-subnet-2.id
}

output "subnet-3" {
  value = aws_subnet.kube-private-subnet-3.id
}
