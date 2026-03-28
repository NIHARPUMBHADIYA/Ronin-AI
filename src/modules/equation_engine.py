"""
Comprehensive Mathematical and Computational Engine
Contains every equation, formula, and calculation method humanity has developed
"""

import sqlite3
import math
import numpy as np
import sympy as sp
from typing import Dict, List, Any, Tuple, Optional, Union
import logging
from pathlib import Path
import json
import re

class UniversalEquationEngine:
    """
    Universal equation engine containing all mathematical formulas and calculations
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_path = Path(config.get('data_dir', 'data')) / 'equations.db'
        self.logger = logging.getLogger(__name__)
        
        # Initialize symbolic math
        self.symbols = {}
        self.equations = {}
        
        # Create database and populate
        self._initialize_database()
        self._populate_equations()
        
        self.logger.info("Universal Equation Engine initialized")
    
    def _initialize_database(self):
        """Initialize the equations database with comprehensive schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Physics equations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS physics_equations (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        variables TEXT,
                        units TEXT,
                        description TEXT,
                        applications TEXT,
                        constants TEXT,
                        derivation TEXT
                    )
                ''')
                
                # Mathematics formulas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS math_formulas (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        domain TEXT,
                        range_val TEXT,
                        conditions TEXT,
                        description TEXT,
                        examples TEXT,
                        proofs TEXT
                    )
                ''')
                
                # Engineering calculations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS engineering_calcs (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        discipline TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        parameters TEXT,
                        units TEXT,
                        safety_factors TEXT,
                        standards TEXT,
                        description TEXT,
                        applications TEXT
                    )
                ''')
                
                # Chemistry equations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS chemistry_equations (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        type TEXT NOT NULL,
                        equation TEXT NOT NULL,
                        reactants TEXT,
                        products TEXT,
                        conditions TEXT,
                        mechanism TEXT,
                        description TEXT,
                        applications TEXT
                    )
                ''')
                
                # Computer science algorithms
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cs_algorithms (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        algorithm TEXT NOT NULL,
                        complexity TEXT,
                        space_complexity TEXT,
                        pseudocode TEXT,
                        implementation TEXT,
                        description TEXT,
                        applications TEXT
                    )
                ''')
                
                # Constants and conversions
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS constants_conversions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        value TEXT NOT NULL,
                        units TEXT NOT NULL,
                        uncertainty TEXT,
                        description TEXT,
                        applications TEXT,
                        notes TEXT
                    )
                ''')
                
                # Biological and medical calculations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS biological_medical (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        variables TEXT,
                        units TEXT,
                        description TEXT,
                        applications TEXT,
                        normal_ranges TEXT,
                        clinical_significance TEXT
                    )
                ''')
                
                # Financial and economic calculations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS financial_economic (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        variables TEXT,
                        units TEXT,
                        description TEXT,
                        applications TEXT,
                        assumptions TEXT,
                        limitations TEXT
                    )
                ''')
                
                # Geological and environmental calculations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS geological_environmental (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        variables TEXT,
                        units TEXT,
                        description TEXT,
                        applications TEXT,
                        environmental_factors TEXT,
                        measurement_methods TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Equations database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise
    
    def _populate_equations(self):
        """Populate database with comprehensive equations and formulas."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Physics equations
                physics_data = self._get_physics_equations()
                cursor.executemany('''
                    INSERT OR REPLACE INTO physics_equations
                    (name, category, formula, variables, units, description, applications, constants, derivation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', physics_data)
                
                # Mathematics formulas
                math_data = self._get_math_formulas()
                cursor.executemany('''
                    INSERT OR REPLACE INTO math_formulas
                    (name, category, formula, domain, range_val, conditions, description, examples, proofs)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', math_data)
                
                # Engineering calculations
                engineering_data = self._get_engineering_calculations()
                cursor.executemany('''
                    INSERT OR REPLACE INTO engineering_calcs
                    (name, discipline, formula, parameters, units, safety_factors, standards, description, applications)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', engineering_data)
                
                # Chemistry equations
                chemistry_data = self._get_chemistry_equations()
                cursor.executemany('''
                    INSERT OR REPLACE INTO chemistry_equations
                    (name, type, equation, reactants, products, conditions, mechanism, description, applications)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', chemistry_data)
                
                # Computer science algorithms
                cs_data = self._get_cs_algorithms()
                cursor.executemany('''
                    INSERT OR REPLACE INTO cs_algorithms
                    (name, category, algorithm, complexity, space_complexity, pseudocode, implementation, description, applications)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', cs_data)
                
                # Constants and conversions
                constants_data = self._get_constants_conversions()
                cursor.executemany('''
                    INSERT OR REPLACE INTO constants_conversions
                    (name, type, value, units, uncertainty, definition, applications, historical_context)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', constants_data)
                
                # Biological and medical calculations
                biological_medical_data = self._get_biological_medical_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO biological_medical
                    (name, category, formula, variables, units, description, applications, normal_ranges, clinical_significance)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', biological_medical_data)
                
                # Financial and economic calculations
                financial_economic_data = self._get_financial_economic_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO financial_economic
                    (name, category, formula, variables, units, description, applications, assumptions, limitations)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', financial_economic_data)
                
                # Geological and environmental calculations
                geological_environmental_data = self._get_geological_environmental_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO geological_environmental
                    (name, category, formula, variables, units, description, applications, environmental_factors, measurement_methods)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', geological_environmental_data)
                
                conn.commit()
                self.logger.info("Initial equation data populated successfully")
                
        except Exception as e:
            self.logger.error(f"Equation population failed: {e}")
    
    def _get_physics_equations(self) -> List[Tuple]:
        """Get comprehensive physics equations."""
        return [
            # name, category, formula, variables, units, description, applications, constants, derivation
            ('Newton\'s Second Law', 'Mechanics', 'F = ma', 'F=force, m=mass, a=acceleration', 'N, kg, m/s²', 'Force equals mass times acceleration', 'All mechanical systems', 'None', 'From Newton\'s laws of motion'),
            ('Kinematic Equation 1', 'Mechanics', 'v = u + at', 'v=final velocity, u=initial velocity, a=acceleration, t=time', 'm/s, m/s², s', 'Velocity-time relationship', 'Motion analysis', 'None', 'Integration of acceleration'),
            ('Kinematic Equation 2', 'Mechanics', 's = ut + (1/2)at²', 's=displacement, u=initial velocity, a=acceleration, t=time', 'm, m/s, m/s², s', 'Displacement-time relationship', 'Projectile motion', 'None', 'Double integration of acceleration'),
            ('Kinematic Equation 3', 'Mechanics', 'v² = u² + 2as', 'v=final velocity, u=initial velocity, a=acceleration, s=displacement', 'm/s, m/s², m', 'Velocity-displacement relationship', 'Energy calculations', 'None', 'Elimination of time from kinematic equations'),
            ('Universal Gravitation', 'Mechanics', 'F = G(m₁m₂)/r²', 'F=gravitational force, G=gravitational constant, m₁,m₂=masses, r=distance', 'N, kg, m', 'Gravitational force between masses', 'Orbital mechanics, astronomy', 'G = 6.674×10⁻¹¹ m³/kg·s²', 'Newton\'s law of universal gravitation'),
            ('Gravitational Potential Energy', 'Mechanics', 'U = -Gm₁m₂/r', 'U=potential energy, G=gravitational constant, m₁,m₂=masses, r=distance', 'J, kg, m', 'Gravitational potential energy', 'Orbital energy calculations', 'G = 6.674×10⁻¹¹ m³/kg·s²', 'Integration of gravitational force'),
            ('Kinetic Energy', 'Mechanics', 'KE = (1/2)mv²', 'KE=kinetic energy, m=mass, v=velocity', 'J, kg, m/s', 'Energy of motion', 'All moving objects', 'None', 'Work-energy theorem'),
            ('Potential Energy', 'Mechanics', 'PE = mgh', 'PE=potential energy, m=mass, g=gravity, h=height', 'J, kg, m/s², m', 'Gravitational potential energy near surface', 'Mechanical systems', 'g = 9.81 m/s²', 'Work done against gravity'),
            ('Conservation of Energy', 'Mechanics', 'E = KE + PE = constant', 'E=total energy, KE=kinetic energy, PE=potential energy', 'J', 'Total mechanical energy conservation', 'All conservative systems', 'None', 'First law of thermodynamics'),
            ('Momentum', 'Mechanics', 'p = mv', 'p=momentum, m=mass, v=velocity', 'kg·m/s', 'Linear momentum', 'Collisions, particle physics', 'None', 'Newton\'s second law'),
            ('Conservation of Momentum', 'Mechanics', 'Σp_initial = Σp_final', 'p=momentum', 'kg·m/s', 'Momentum conservation in isolated systems', 'Collisions, explosions', 'None', 'Newton\'s third law'),
            ('Angular Momentum', 'Mechanics', 'L = Iω = r × p', 'L=angular momentum, I=moment of inertia, ω=angular velocity, r=radius, p=momentum', 'kg·m²/s', 'Rotational momentum', 'Rotating systems', 'None', 'Cross product of position and momentum'),
            ('Torque', 'Mechanics', 'τ = r × F = Iα', 'τ=torque, r=radius, F=force, I=moment of inertia, α=angular acceleration', 'N·m, kg·m²/s²', 'Rotational force', 'Rotating machinery', 'None', 'Rotational analog of Newton\'s second law'),
            ('Moment of Inertia (Point Mass)', 'Mechanics', 'I = mr²', 'I=moment of inertia, m=mass, r=distance from axis', 'kg·m²', 'Rotational inertia of point mass', 'Rotational dynamics', 'None', 'Definition of moment of inertia'),
            ('Centripetal Force', 'Mechanics', 'F_c = mv²/r = mω²r', 'F_c=centripetal force, m=mass, v=velocity, r=radius, ω=angular velocity', 'N, kg, m/s, m, rad/s', 'Force toward center of circular motion', 'Circular motion', 'None', 'Newton\'s second law in circular motion'),
            ('Simple Harmonic Motion', 'Mechanics', 'x = A cos(ωt + φ)', 'x=displacement, A=amplitude, ω=angular frequency, t=time, φ=phase', 'm, rad/s, s, rad', 'Oscillatory motion', 'Springs, pendulums, waves', 'None', 'Solution to differential equation F = -kx'),
            ('Hooke\'s Law', 'Mechanics', 'F = -kx', 'F=restoring force, k=spring constant, x=displacement', 'N, N/m, m', 'Elastic restoring force', 'Springs, elastic materials', 'None', 'Linear elasticity'),
            ('Period of Simple Pendulum', 'Mechanics', 'T = 2π√(L/g)', 'T=period, L=length, g=gravitational acceleration', 's, m, m/s²', 'Oscillation period of pendulum', 'Timekeeping, seismology', 'g = 9.81 m/s²', 'Small angle approximation of pendulum motion'),
            ('Wave Equation', 'Waves', 'v = fλ', 'v=wave speed, f=frequency, λ=wavelength', 'm/s, Hz, m', 'Relationship between wave properties', 'All wave phenomena', 'None', 'Definition of wave speed'),
            ('Doppler Effect', 'Waves', 'f\' = f(v ± v_r)/(v ± v_s)', 'f\'=observed frequency, f=source frequency, v=wave speed, v_r=receiver velocity, v_s=source velocity', 'Hz, m/s', 'Frequency shift due to relative motion', 'Radar, astronomy, medical imaging', 'None', 'Wave equation with moving source/observer'),
            ('Coulomb\'s Law', 'Electromagnetism', 'F = k(q₁q₂)/r²', 'F=electric force, k=Coulomb constant, q₁,q₂=charges, r=distance', 'N, C, m', 'Electric force between charges', 'Electrostatics', 'k = 8.99×10⁹ N·m²/C²', 'Fundamental law of electrostatics'),
            ('Electric Field', 'Electromagnetism', 'E = F/q = kQ/r²', 'E=electric field, F=force, q=test charge, Q=source charge, r=distance', 'N/C, V/m', 'Electric field strength', 'All electrical phenomena', 'k = 8.99×10⁹ N·m²/C²', 'Force per unit charge'),
            ('Electric Potential', 'Electromagnetism', 'V = kQ/r', 'V=electric potential, k=Coulomb constant, Q=charge, r=distance', 'V, J/C', 'Electric potential energy per unit charge', 'Electrical circuits', 'k = 8.99×10⁹ N·m²/C²', 'Work done per unit charge'),
            ('Ohm\'s Law', 'Electromagnetism', 'V = IR', 'V=voltage, I=current, R=resistance', 'V, A, Ω', 'Relationship between voltage, current, and resistance', 'All electrical circuits', 'None', 'Linear relationship in ohmic materials'),
            ('Electrical Power', 'Electromagnetism', 'P = VI = I²R = V²/R', 'P=power, V=voltage, I=current, R=resistance', 'W, V, A, Ω', 'Electrical power dissipation', 'Electrical systems', 'None', 'Energy per unit time'),
            ('Capacitance', 'Electromagnetism', 'C = Q/V', 'C=capacitance, Q=charge, V=voltage', 'F, C, V', 'Charge storage capacity', 'Capacitors, energy storage', 'None', 'Definition of capacitance'),
            ('Energy in Capacitor', 'Electromagnetism', 'U = (1/2)CV² = (1/2)QV', 'U=energy, C=capacitance, V=voltage, Q=charge', 'J, F, V, C', 'Energy stored in electric field', 'Energy storage systems', 'None', 'Work done to charge capacitor'),
            ('Magnetic Force on Moving Charge', 'Electromagnetism', 'F = q(v × B)', 'F=magnetic force, q=charge, v=velocity, B=magnetic field', 'N, C, m/s, T', 'Force on charge in magnetic field', 'Particle accelerators, motors', 'None', 'Lorentz force law'),
            ('Magnetic Force on Current', 'Electromagnetism', 'F = IL × B', 'F=force, I=current, L=length vector, B=magnetic field', 'N, A, m, T', 'Force on current-carrying conductor', 'Electric motors, generators', 'None', 'Force on moving charges in conductor'),
            ('Faraday\'s Law', 'Electromagnetism', 'ε = -dΦ/dt', 'ε=induced EMF, Φ=magnetic flux, t=time', 'V, Wb, s', 'Electromagnetic induction', 'Generators, transformers', 'None', 'Change in magnetic flux induces EMF'),
            ('Lenz\'s Law', 'Electromagnetism', 'Direction opposes change', 'Qualitative law', 'None', 'Direction of induced current', 'Electromagnetic induction', 'None', 'Conservation of energy in electromagnetic systems'),
            
            # Thermodynamics
            ('First Law of Thermodynamics', 'Thermodynamics', 'ΔU = Q - W', 'ΔU=change in internal energy, Q=heat added, W=work done by system', 'J', 'Energy conservation in thermodynamic processes', 'Heat engines, refrigeration', 'None', 'Conservation of energy'),
            ('Second Law of Thermodynamics', 'Thermodynamics', 'ΔS ≥ 0', 'ΔS=change in entropy', 'J/K', 'Entropy always increases in isolated systems', 'Heat engines, information theory', 'None', 'Statistical mechanics'),
            ('Ideal Gas Law', 'Thermodynamics', 'PV = nRT', 'P=pressure, V=volume, n=moles, R=gas constant, T=temperature', 'Pa, m³, mol, J/(mol·K), K', 'Equation of state for ideal gas', 'Gas calculations, atmospheric science', 'R = 8.314 J/(mol·K)', 'Kinetic theory of gases'),
            ('Heat Capacity', 'Thermodynamics', 'C = Q/ΔT', 'C=heat capacity, Q=heat, ΔT=temperature change', 'J/K', 'Heat required to change temperature', 'Thermal analysis', 'None', 'Definition of heat capacity'),
            ('Stefan-Boltzmann Law', 'Thermodynamics', 'P = σAT⁴', 'P=radiated power, σ=Stefan-Boltzmann constant, A=area, T=temperature', 'W, W/(m²·K⁴), m², K', 'Blackbody radiation power', 'Thermal radiation, astronomy', 'σ = 5.67×10⁻⁸ W/(m²·K⁴)', 'Planck\'s law integration'),
            ('Carnot Efficiency', 'Thermodynamics', 'η = 1 - T_c/T_h', 'η=efficiency, T_c=cold reservoir temperature, T_h=hot reservoir temperature', 'Dimensionless, K', 'Maximum theoretical efficiency of heat engine', 'Power generation', 'None', 'Second law of thermodynamics'),
            
            # Quantum Mechanics
            ('Planck\'s Equation', 'Quantum Mechanics', 'E = hf', 'E=photon energy, h=Planck constant, f=frequency', 'J, J·s, Hz', 'Energy of electromagnetic radiation quantum', 'Quantum physics, spectroscopy', 'h = 6.626×10⁻³⁴ J·s', 'Quantum theory foundation'),
            ('de Broglie Wavelength', 'Quantum Mechanics', 'λ = h/p', 'λ=wavelength, h=Planck constant, p=momentum', 'm, J·s, kg·m/s', 'Matter wave wavelength', 'Electron microscopy, quantum mechanics', 'h = 6.626×10⁻³⁴ J·s', 'Wave-particle duality'),
            ('Heisenberg Uncertainty Principle', 'Quantum Mechanics', 'Δx·Δp ≥ ℏ/2', 'Δx=position uncertainty, Δp=momentum uncertainty, ℏ=reduced Planck constant', 'm, kg·m/s, J·s', 'Fundamental limit on measurement precision', 'Quantum mechanics', 'ℏ = 1.055×10⁻³⁴ J·s', 'Quantum mechanics foundation'),
            ('Schrödinger Equation', 'Quantum Mechanics', 'iℏ∂ψ/∂t = Ĥψ', 'ψ=wavefunction, ℏ=reduced Planck constant, Ĥ=Hamiltonian operator', 'Various', 'Time evolution of quantum systems', 'All quantum mechanics', 'ℏ = 1.055×10⁻³⁴ J·s', 'Fundamental equation of quantum mechanics'),
            
            # Relativity
            ('Mass-Energy Equivalence', 'Relativity', 'E = mc²', 'E=energy, m=mass, c=speed of light', 'J, kg, m/s', 'Equivalence of mass and energy', 'Nuclear physics, cosmology', 'c = 2.998×10⁸ m/s', 'Special relativity'),
            ('Lorentz Factor', 'Relativity', 'γ = 1/√(1-v²/c²)', 'γ=Lorentz factor, v=velocity, c=speed of light', 'Dimensionless, m/s', 'Time dilation and length contraction factor', 'High-speed physics', 'c = 2.998×10⁸ m/s', 'Special relativity kinematics'),
            ('Time Dilation', 'Relativity', 'Δt = γΔt₀', 'Δt=dilated time, γ=Lorentz factor, Δt₀=proper time', 's', 'Time passes slower for moving objects', 'GPS satellites, particle physics', 'None', 'Special relativity'),
            ('Length Contraction', 'Relativity', 'L = L₀/γ', 'L=contracted length, L₀=proper length, γ=Lorentz factor', 'm', 'Length contracts in direction of motion', 'High-speed physics', 'None', 'Special relativity'),
            ('Relativistic Momentum', 'Relativity', 'p = γmv', 'p=momentum, γ=Lorentz factor, m=rest mass, v=velocity', 'kg·m/s', 'Momentum at relativistic speeds', 'Particle accelerators', 'None', 'Special relativity dynamics'),
            ('Schwarzschild Radius', 'Relativity', 'r_s = 2GM/c²', 'r_s=Schwarzschild radius, G=gravitational constant, M=mass, c=speed of light', 'm, m³/(kg·s²), kg, m/s', 'Event horizon radius of black hole', 'Black hole physics', 'G = 6.674×10⁻¹¹ m³/(kg·s²), c = 2.998×10⁸ m/s', 'General relativity'),
            
            # Fluid Mechanics
            ('Continuity Equation', 'Fluid Mechanics', 'ρ₁A₁v₁ = ρ₂A₂v₂', 'ρ=density, A=cross-sectional area, v=velocity', 'kg/m³, m², m/s', 'Mass conservation in fluid flow', 'Pipe flow, aerodynamics', 'None', 'Conservation of mass'),
            ('Bernoulli\'s Equation', 'Fluid Mechanics', 'P + ½ρv² + ρgh = constant', 'P=pressure, ρ=density, v=velocity, g=gravity, h=height', 'Pa, kg/m³, m/s, m/s², m', 'Energy conservation in fluid flow', 'Aerodynamics, hydraulics', 'g = 9.81 m/s²', 'Conservation of energy in fluids'),
            ('Reynolds Number', 'Fluid Mechanics', 'Re = ρvL/μ', 'Re=Reynolds number, ρ=density, v=velocity, L=characteristic length, μ=dynamic viscosity', 'Dimensionless', 'Flow regime characterization', 'Fluid flow analysis', 'None', 'Ratio of inertial to viscous forces'),
            ('Drag Force', 'Fluid Mechanics', 'F_d = ½ρv²C_dA', 'F_d=drag force, ρ=fluid density, v=velocity, C_d=drag coefficient, A=reference area', 'N, kg/m³, m/s, m²', 'Resistance force in fluid flow', 'Aerodynamics, vehicle design', 'None', 'Momentum transfer in boundary layer'),
            ('Lift Force', 'Fluid Mechanics', 'F_l = ½ρv²C_lA', 'F_l=lift force, ρ=fluid density, v=velocity, C_l=lift coefficient, A=wing area', 'N, kg/m³, m/s, m²', 'Upward force on airfoil', 'Aircraft design', 'None', 'Circulation and pressure difference'),
            
            # Optics
            ('Snell\'s Law', 'Optics', 'n₁sin(θ₁) = n₂sin(θ₂)', 'n=refractive index, θ=angle from normal', 'Dimensionless, radians', 'Light refraction at interface', 'Lens design, fiber optics', 'None', 'Fermat\'s principle'),
            ('Lens Equation', 'Optics', '1/f = 1/d_o + 1/d_i', 'f=focal length, d_o=object distance, d_i=image distance', 'm', 'Image formation by thin lens', 'Optical instruments', 'None', 'Geometric optics'),
            ('Magnification', 'Optics', 'M = -d_i/d_o = h_i/h_o', 'M=magnification, d_i=image distance, d_o=object distance, h_i=image height, h_o=object height', 'Dimensionless', 'Image size relative to object', 'Microscopes, telescopes', 'None', 'Similar triangles in optics'),
            ('Diffraction Grating', 'Optics', 'dsin(θ) = mλ', 'd=grating spacing, θ=diffraction angle, m=order, λ=wavelength', 'm, radians, m', 'Constructive interference condition', 'Spectroscopy', 'None', 'Wave interference'),
            ('Rayleigh Criterion', 'Optics', 'θ = 1.22λ/D', 'θ=angular resolution, λ=wavelength, D=aperture diameter', 'radians, m', 'Minimum resolvable angle', 'Telescope design', 'None', 'Diffraction limit'),
            
            # Nuclear Physics
            ('Radioactive Decay', 'Nuclear Physics', 'N(t) = N₀e^(-λt)', 'N(t)=number at time t, N₀=initial number, λ=decay constant, t=time', 'Dimensionless, s⁻¹, s', 'Exponential decay of radioactive nuclei', 'Nuclear medicine, dating', 'None', 'Statistical decay process'),
            ('Half-Life', 'Nuclear Physics', 't₁/₂ = ln(2)/λ', 't₁/₂=half-life, λ=decay constant', 's, s⁻¹', 'Time for half of nuclei to decay', 'Radioactive dating', 'ln(2) = 0.693', 'Exponential decay'),
            ('Binding Energy', 'Nuclear Physics', 'BE = (Zm_p + Nm_n - M)c²', 'BE=binding energy, Z=proton number, N=neutron number, m_p=proton mass, m_n=neutron mass, M=nuclear mass, c=speed of light', 'J, kg, m/s', 'Energy holding nucleus together', 'Nuclear reactions', 'c = 2.998×10⁸ m/s', 'Mass-energy equivalence'),
            ('Nuclear Reaction Q-value', 'Nuclear Physics', 'Q = (m_initial - m_final)c²', 'Q=reaction energy, m=mass, c=speed of light', 'J, kg, m/s', 'Energy released in nuclear reaction', 'Nuclear power, weapons', 'c = 2.998×10⁸ m/s', 'Conservation of mass-energy')
        ]
    
    def _get_math_formulas(self) -> List[Tuple]:
        """Get comprehensive mathematical formulas."""
        return [
            # name, category, formula, domain, range_val, conditions, description, examples, proofs
            ('Quadratic Formula', 'Algebra', 'x = (-b ± √(b²-4ac))/(2a)', 'Real numbers', 'Real or complex', 'a ≠ 0', 'Solutions to quadratic equations', 'ax² + bx + c = 0', 'Completing the square'),
            ('Pythagorean Theorem', 'Geometry', 'a² + b² = c²', 'Positive reals', 'Positive reals', 'Right triangle', 'Relationship between sides of right triangle', '3² + 4² = 5²', 'Geometric proof'),
            ('Distance Formula', 'Geometry', 'd = √((x₂-x₁)² + (y₂-y₁)²)', 'Real numbers', 'Non-negative reals', 'None', 'Distance between two points', 'd((0,0),(3,4)) = 5', 'Pythagorean theorem'),
            ('Slope Formula', 'Geometry', 'm = (y₂-y₁)/(x₂-x₁)', 'Real numbers', 'Real numbers', 'x₁ ≠ x₂', 'Slope of line through two points', 'm = Δy/Δx', 'Definition of slope'),
            ('Circle Equation', 'Geometry', '(x-h)² + (y-k)² = r²', 'Real numbers', 'Non-negative reals', 'r > 0', 'Equation of circle with center (h,k) and radius r', 'x² + y² = 1', 'Distance formula'),
            ('Area of Circle', 'Geometry', 'A = πr²', 'Positive reals', 'Positive reals', 'r > 0', 'Area enclosed by circle', 'A = π(5)² = 25π', 'Integration in polar coordinates'),
            ('Circumference of Circle', 'Geometry', 'C = 2πr', 'Positive reals', 'Positive reals', 'r > 0', 'Perimeter of circle', 'C = 2π(5) = 10π', 'Definition of π'),
            ('Volume of Sphere', 'Geometry', 'V = (4/3)πr³', 'Positive reals', 'Positive reals', 'r > 0', 'Volume of sphere', 'V = (4/3)π(3)³ = 36π', 'Triple integration'),
            ('Surface Area of Sphere', 'Geometry', 'SA = 4πr²', 'Positive reals', 'Positive reals', 'r > 0', 'Surface area of sphere', 'SA = 4π(3)² = 36π', 'Surface integration'),
            ('Law of Cosines', 'Trigonometry', 'c² = a² + b² - 2ab cos(C)', 'Positive reals', 'Positive reals', 'Triangle inequality', 'Generalization of Pythagorean theorem', 'Any triangle', 'Geometric proof'),
            ('Law of Sines', 'Trigonometry', 'a/sin(A) = b/sin(B) = c/sin(C)', 'Positive reals', 'Positive reals', 'Valid triangle', 'Relationship between sides and angles', 'Any triangle', 'Area formula'),
            ('Sine Function', 'Trigonometry', 'sin(θ) = opposite/hypotenuse', '[-1, 1]', '[-1, 1]', 'Right triangle', 'Trigonometric ratio', 'sin(30°) = 1/2', 'Unit circle definition'),
            ('Cosine Function', 'Trigonometry', 'cos(θ) = adjacent/hypotenuse', '[-1, 1]', '[-1, 1]', 'Right triangle', 'Trigonometric ratio', 'cos(60°) = 1/2', 'Unit circle definition'),
            ('Tangent Function', 'Trigonometry', 'tan(θ) = opposite/adjacent = sin(θ)/cos(θ)', 'All reals except odd multiples of π/2', 'All reals', 'cos(θ) ≠ 0', 'Trigonometric ratio', 'tan(45°) = 1', 'Definition from sine and cosine'),
            ('Euler\'s Identity', 'Complex Analysis', 'e^(iπ) + 1 = 0', 'Complex numbers', 'Complex numbers', 'None', 'Most beautiful equation in mathematics', 'Links e, i, π, 1, 0', 'Euler\'s formula'),
            ('Euler\'s Formula', 'Complex Analysis', 'e^(iθ) = cos(θ) + i sin(θ)', 'Real θ', 'Unit circle in complex plane', 'None', 'Exponential form of complex numbers', 'e^(iπ/2) = i', 'Taylor series'),
            ('Derivative Definition', 'Calculus', 'f\'(x) = lim[h→0] (f(x+h) - f(x))/h', 'Differentiable functions', 'Real numbers', 'Limit exists', 'Rate of change at a point', 'd/dx(x²) = 2x', 'Limit definition'),
            ('Power Rule', 'Calculus', 'd/dx(x^n) = nx^(n-1)', 'Real numbers', 'Real numbers', 'n ≠ 0 for x = 0', 'Derivative of power function', 'd/dx(x³) = 3x²', 'Binomial theorem limit'),
            ('Product Rule', 'Calculus', 'd/dx(uv) = u\'v + uv\'', 'Differentiable functions', 'Real numbers', 'Both functions differentiable', 'Derivative of product', 'd/dx(x sin(x)) = sin(x) + x cos(x)', 'Limit of difference quotient'),
            ('Chain Rule', 'Calculus', 'd/dx(f(g(x))) = f\'(g(x)) · g\'(x)', 'Composite functions', 'Real numbers', 'Both functions differentiable', 'Derivative of composition', 'd/dx(sin(x²)) = 2x cos(x²)', 'Limit definition'),
            ('Fundamental Theorem of Calculus', 'Calculus', '∫[a to b] f\'(x)dx = f(b) - f(a)', 'Continuous functions', 'Real numbers', 'f differentiable on [a,b]', 'Connection between derivatives and integrals', '∫[0 to 1] 2x dx = 1', 'Definition of definite integral'),
            ('Integration by Parts', 'Calculus', '∫ u dv = uv - ∫ v du', 'Integrable functions', 'Functions', 'u and v differentiable', 'Integration technique', '∫ x e^x dx = xe^x - e^x + C', 'Product rule in reverse'),
            ('L\'Hôpital\'s Rule', 'Calculus', 'lim[x→a] f(x)/g(x) = lim[x→a] f\'(x)/g\'(x)', 'Differentiable functions', 'Real numbers or ∞', 'Indeterminate form 0/0 or ∞/∞', 'Evaluate indeterminate limits', 'lim[x→0] sin(x)/x = 1', 'Mean value theorem'),
            ('Taylor Series', 'Calculus', 'f(x) = Σ[n=0 to ∞] f^(n)(a)(x-a)^n/n!', 'Infinitely differentiable', 'Convergent series', 'Series converges', 'Power series expansion', 'e^x = Σ x^n/n!', 'Repeated differentiation'),
            ('Maclaurin Series', 'Calculus', 'f(x) = Σ[n=0 to ∞] f^(n)(0)x^n/n!', 'Infinitely differentiable at 0', 'Convergent series', 'Series converges', 'Taylor series at x=0', 'sin(x) = Σ (-1)^n x^(2n+1)/(2n+1)!', 'Taylor series with a=0'),
            ('Arithmetic Mean', 'Statistics', 'μ = (Σx_i)/n', 'Real numbers', 'Real numbers', 'n > 0', 'Average of data set', '(1+2+3)/3 = 2', 'Definition of average'),
            ('Standard Deviation', 'Statistics', 'σ = √(Σ(x_i - μ)²/n)', 'Real numbers', 'Non-negative reals', 'n > 0', 'Measure of data spread', 'Population standard deviation', 'Variance definition'),
            ('Normal Distribution', 'Statistics', 'f(x) = (1/(σ√(2π)))e^(-(x-μ)²/(2σ²))', 'Real numbers', '[0, 1/(σ√(2π))]', 'σ > 0', 'Bell curve probability density', 'Standard normal: μ=0, σ=1', 'Central limit theorem'),
            ('Binomial Probability', 'Statistics', 'P(X=k) = C(n,k)p^k(1-p)^(n-k)', 'Non-negative integers', '[0, 1]', '0 ≤ p ≤ 1, k ≤ n', 'Probability of k successes in n trials', 'Coin flips', 'Bernoulli trials'),
            ('Combination Formula', 'Combinatorics', 'C(n,k) = n!/(k!(n-k)!)', 'Non-negative integers', 'Non-negative integers', 'k ≤ n', 'Number of ways to choose k from n', 'C(5,2) = 10', 'Counting principle'),
            ('Permutation Formula', 'Combinatorics', 'P(n,k) = n!/(n-k)!', 'Non-negative integers', 'Non-negative integers', 'k ≤ n', 'Number of ordered arrangements', 'P(5,2) = 20', 'Counting principle'),
            ('Fibonacci Sequence', 'Number Theory', 'F_n = F_(n-1) + F_(n-2)', 'Non-negative integers', 'Non-negative integers', 'F_0=0, F_1=1', 'Recursive sequence', '0,1,1,2,3,5,8,13,...', 'Recurrence relation'),
            ('Golden Ratio', 'Number Theory', 'φ = (1 + √5)/2 ≈ 1.618', 'Positive reals', 'Positive reals', 'None', 'Divine proportion', 'φ² = φ + 1', 'Quadratic equation solution'),
            ('Prime Number Theorem', 'Number Theory', 'π(x) ~ x/ln(x)', 'Positive reals', 'Non-negative reals', 'x → ∞', 'Asymptotic distribution of primes', 'Density of primes decreases', 'Complex analysis proof'),
            ('Riemann Zeta Function', 'Number Theory', 'ζ(s) = Σ[n=1 to ∞] 1/n^s', 'Complex numbers', 'Complex numbers', 'Re(s) > 1 for convergence', 'Analytic continuation of harmonic series', 'ζ(2) = π²/6', 'Euler\'s method'),
            ('Bayes\' Theorem', 'Probability', 'P(A|B) = P(B|A)P(A)/P(B)', '[0, 1]', '[0, 1]', 'P(B) > 0', 'Conditional probability update', 'Medical diagnosis', 'Definition of conditional probability'),
            ('Central Limit Theorem', 'Probability', 'X̄ ~ N(μ, σ²/n) as n → ∞', 'Random variables', 'Normal distribution', 'Independent, finite variance', 'Sample means approach normal distribution', 'Polling, quality control', 'Characteristic functions')
        ]
    
    def _get_engineering_calculations(self) -> List[Tuple]:
        """Get comprehensive engineering calculations."""
        return [
            # name, discipline, formula, parameters, units, safety_factors, standards, description, applications
            ('Beam Bending Stress', 'Structural', 'σ = My/I', 'σ=stress, M=moment, y=distance from neutral axis, I=moment of inertia', 'Pa, N·m, m, m⁴', '2.0-4.0', 'AISC, Eurocode', 'Maximum stress in bent beam', 'Building design, bridges'),
            ('Euler Buckling Load', 'Structural', 'P_cr = π²EI/(KL)²', 'P_cr=critical load, E=elastic modulus, I=moment of inertia, K=effective length factor, L=length', 'N, Pa, m⁴, m', '2.5-3.0', 'AISC 360', 'Critical buckling load for columns', 'Column design'),
            ('Heat Transfer Conduction', 'Thermal', 'q = -kA(dT/dx)', 'q=heat flux, k=thermal conductivity, A=area, dT/dx=temperature gradient', 'W, W/(m·K), m², K/m', 'None', 'ASHRAE', 'Fourier\'s law of heat conduction', 'Thermal analysis'),
            ('Pump Power', 'Fluid Mechanics', 'P = ρgQH/η', 'P=power, ρ=density, g=gravity, Q=flow rate, H=head, η=efficiency', 'W, kg/m³, m/s², m³/s, m', 'None', 'Hydraulic Institute', 'Power required for pumping', 'Pump selection'),
            ('Electrical Power (AC)', 'Electrical', 'P = VIcos(φ)', 'P=real power, V=voltage, I=current, φ=phase angle', 'W, V, A, rad', 'None', 'IEEE standards', 'AC power calculation', 'Power systems'),
            ('Concrete Compressive Strength', 'Materials', 'f\'_c = P/A', 'f\'_c=compressive strength, P=maximum load, A=cross-sectional area', 'Pa, N, m²', '1.5-2.0', 'ACI 318', 'Concrete strength', 'Structural design')
        ]
    
    def _get_chemistry_equations(self) -> List[Tuple]:
        """Get comprehensive chemistry equations."""
        return [
            # name, type, equation, reactants, products, conditions, mechanism, description, applications
            ('Ideal Gas Law', 'Physical Chemistry', 'PV = nRT', 'Gas molecules', 'Pressure-volume relationship', 'Ideal conditions', 'Kinetic theory', 'Equation of state for ideal gas', 'Gas calculations'),
            ('Arrhenius Equation', 'Kinetics', 'k = Ae^(-Ea/RT)', 'Reactants', 'Rate constant', 'Temperature dependent', 'Activation energy', 'Temperature dependence of reaction rate', 'Reaction kinetics'),
            ('Henderson-Hasselbalch', 'Acid-Base', 'pH = pKa + log([A⁻]/[HA])', 'Weak acid/base', 'pH value', 'Aqueous solution', 'Equilibrium', 'pH of buffer solutions', 'Biochemistry, analytical chemistry'),
            ('Nernst Equation', 'Electrochemistry', 'E = E° - (RT/nF)ln(Q)', 'Oxidized/reduced species', 'Cell potential', 'Non-standard conditions', 'Electron transfer', 'Electrode potential under non-standard conditions', 'Batteries, corrosion'),
            ('Beer-Lambert Law', 'Spectroscopy', 'A = εbc', 'Light, sample', 'Absorbance', 'Dilute solutions', 'Light absorption', 'Relationship between absorbance and concentration', 'Analytical chemistry, spectroscopy')
        ]
    
    def _get_cs_algorithms(self) -> List[Tuple]:
        """Get comprehensive computer science algorithms."""
        return [
            # name, category, algorithm, complexity, space_complexity, pseudocode, implementation, description, applications
            ('Binary Search', 'Search', 'Divide and conquer on sorted array', 'O(log n)', 'O(1)', 'Compare middle element, recurse on half', 'Recursive or iterative', 'Efficient search in sorted data', 'Database indexing, search engines'),
            ('Quick Sort', 'Sorting', 'Divide and conquer with pivot', 'O(n log n) average, O(n²) worst', 'O(log n)', 'Choose pivot, partition, recurse', 'In-place partitioning', 'Fast general-purpose sorting', 'Operating systems, databases'),
            ('Merge Sort', 'Sorting', 'Divide and conquer with merging', 'O(n log n)', 'O(n)', 'Divide array, sort halves, merge', 'Stable sorting algorithm', 'Guaranteed O(n log n) performance', 'External sorting, stable sorting'),
            ('Dijkstra\'s Algorithm', 'Graph', 'Shortest path with priority queue', 'O((V + E) log V)', 'O(V)', 'Maintain distances, update neighbors', 'Priority queue implementation', 'Single-source shortest paths', 'GPS navigation, network routing'),
            ('Dynamic Programming', 'Optimization', 'Break problem into subproblems', 'Problem dependent', 'Problem dependent', 'Memoization or tabulation', 'Bottom-up or top-down', 'Optimal substructure problems', 'Algorithm optimization, AI'),
            ('Hash Table', 'Data Structure', 'Key-value mapping with hash function', 'O(1) average', 'O(n)', 'Hash function, collision resolution', 'Array with linked lists', 'Fast key-value lookups', 'Databases, caching, compilers')
        ]
    
    def _get_constants_conversions(self) -> List[Tuple]:
        """Get comprehensive constants and conversions."""
        return [
            # name, type, value, units, uncertainty, definition, applications, historical_context
            ('Speed of Light', 'Physical Constant', '299792458', 'm/s', 'Exact by definition', 'Speed of electromagnetic radiation in vacuum', 'Relativity, optics, telecommunications', 'Defined in 1983 to fix meter definition'),
            ('Planck Constant', 'Physical Constant', '6.62607015×10⁻³⁴', 'J·s', 'Exact by definition', 'Quantum of electromagnetic action', 'Quantum mechanics, spectroscopy', 'Discovered by Max Planck in 1900'),
            ('Avogadro Number', 'Physical Constant', '6.02214076×10²³', 'mol⁻¹', 'Exact by definition', 'Number of particles in one mole', 'Chemistry, atomic physics', 'Named after Amedeo Avogadro'),
            ('Gravitational Constant', 'Physical Constant', '6.67430×10⁻¹¹', 'm³/(kg·s²)', '±0.00015×10⁻¹¹', 'Universal gravitational constant', 'Gravitation, cosmology', 'Measured by Henry Cavendish in 1798'),
            ('Elementary Charge', 'Physical Constant', '1.602176634×10⁻¹⁹', 'C', 'Exact by definition', 'Electric charge of proton', 'Electromagnetism, particle physics', 'Measured by Robert Millikan in 1909'),
            ('Meter to Feet', 'Length Conversion', '3.28084', 'ft/m', 'Exact', 'Imperial to metric length conversion', 'Engineering, construction', 'Based on international foot definition'),
            ('Kilogram to Pounds', 'Mass Conversion', '2.20462', 'lb/kg', 'Exact', 'Metric to imperial mass conversion', 'Commerce, engineering', 'Based on avoirdupois pound'),
            ('Celsius to Fahrenheit', 'Temperature Conversion', 'F = 9C/5 + 32', '°F', 'Exact', 'Temperature scale conversion', 'Weather, cooking, science', 'Fahrenheit scale from 1724'),
            ('Pascal to PSI', 'Pressure Conversion', '0.000145038', 'psi/Pa', 'Exact', 'Metric to imperial pressure conversion', 'Engineering, automotive', 'Pounds per square inch'),
            ('Joule to BTU', 'Energy Conversion', '0.000947817', 'BTU/J', 'Exact', 'Metric to imperial energy conversion', 'HVAC, energy systems', 'British Thermal Unit')
        ]
    
    def _get_biological_medical_data(self) -> List[Tuple]:
        """Get biological and medical calculations."""
        return [
            # name, category, formula, variables, units, description, applications, normal_ranges, clinical_significance
            ('Body Mass Index', 'Anthropometry', 'BMI = weight / height²', 'weight=body weight, height=height', 'kg/m²', 'Body mass index calculation', 'Health assessment, nutrition', '18.5-24.9 kg/m²', 'Obesity screening'),
            ('Cardiac Output', 'Cardiovascular', 'CO = HR × SV', 'CO=cardiac output, HR=heart rate, SV=stroke volume', 'L/min', 'Volume of blood pumped per minute', 'Cardiac function assessment', '4-8 L/min', 'Heart failure diagnosis'),
            ('Glomerular Filtration Rate', 'Renal', 'GFR = (140-age)×weight/(72×creatinine)', 'age=years, weight=kg, creatinine=mg/dL', 'mL/min/1.73m²', 'Kidney function assessment', 'Nephrology, drug dosing', '>90 mL/min/1.73m²', 'Chronic kidney disease staging'),
            ('Basal Metabolic Rate', 'Metabolism', 'BMR = 88.362 + 13.397×weight + 4.799×height - 5.677×age', 'weight=kg, height=cm, age=years', 'kcal/day', 'Energy expenditure at rest', 'Nutrition planning', '1200-2000 kcal/day', 'Metabolic disorders'),
            ('Oxygen Saturation', 'Respiratory', 'SaO₂ = (HbO₂ / (HbO₂ + Hb)) × 100', 'HbO₂=oxyhemoglobin, Hb=deoxyhemoglobin', '%', 'Percentage of oxygen-saturated hemoglobin', 'Respiratory monitoring', '95-100%', 'Hypoxemia detection'),
            ('Blood Pressure Mean', 'Cardiovascular', 'MAP = DBP + (SBP - DBP)/3', 'MAP=mean arterial pressure, DBP=diastolic, SBP=systolic', 'mmHg', 'Average arterial pressure during cardiac cycle', 'Hemodynamic monitoring', '70-100 mmHg', 'Perfusion assessment'),
            ('Creatinine Clearance', 'Renal', 'CrCl = (urine_Cr × urine_volume) / (serum_Cr × time)', 'urine_Cr=urine creatinine, serum_Cr=serum creatinine', 'mL/min', 'Kidney filtration function', 'Renal function testing', '90-120 mL/min', 'Kidney disease progression'),
            ('Alveolar Gas Equation', 'Respiratory', 'PAO₂ = FiO₂(Patm - PH₂O) - PaCO₂/RQ', 'FiO₂=fraction inspired oxygen, Patm=atmospheric pressure, PH₂O=water vapor pressure, PaCO₂=arterial CO₂, RQ=respiratory quotient', 'mmHg', 'Alveolar oxygen partial pressure', 'Pulmonary function', '100-110 mmHg', 'Gas exchange disorders'),
            ('Pharmacokinetic Half-life', 'Pharmacology', 't₁/₂ = 0.693 × Vd / Cl', 't₁/₂=half-life, Vd=volume of distribution, Cl=clearance', 'hours', 'Time for drug concentration to decrease by half', 'Drug dosing', 'Drug-specific', 'Dosing interval determination'),
            ('Henderson-Hasselbalch', 'Acid-Base', 'pH = pKa + log([A⁻]/[HA])', 'pH=acidity, pKa=acid dissociation constant, [A⁻]=conjugate base, [HA]=weak acid', 'pH units', 'Relationship between pH and buffer components', 'Acid-base balance', '7.35-7.45', 'Metabolic acidosis/alkalosis')
        ]
    
    def _get_financial_economic_data(self) -> List[Tuple]:
        """Get financial and economic calculations."""
        return [
            # name, category, formula, variables, units, description, applications, assumptions, limitations
            ('Present Value', 'Time Value of Money', 'PV = FV / (1 + r)ⁿ', 'PV=present value, FV=future value, r=discount rate, n=periods', 'Currency', 'Current worth of future cash flow', 'Investment analysis', 'Constant discount rate', 'Inflation effects'),
            ('Future Value', 'Time Value of Money', 'FV = PV × (1 + r)ⁿ', 'PV=present value, r=interest rate, n=periods', 'Currency', 'Value of investment after compound growth', 'Savings planning', 'Constant interest rate', 'Market volatility'),
            ('Net Present Value', 'Capital Budgeting', 'NPV = Σ(CFt / (1 + r)ᵗ) - Initial Investment', 'CFt=cash flow at time t, r=discount rate', 'Currency', 'Profitability of investment project', 'Project evaluation', 'Known cash flows', 'Estimation accuracy'),
            ('Internal Rate of Return', 'Capital Budgeting', 'NPV = 0 = Σ(CFt / (1 + IRR)ᵗ)', 'CFt=cash flow at time t, IRR=internal rate of return', '%', 'Discount rate making NPV zero', 'Investment comparison', 'Reinvestment at IRR', 'Multiple IRRs possible'),
            ('Black-Scholes Option Price', 'Derivatives', 'C = S₀N(d₁) - Ke⁻ʳᵀN(d₂)', 'S₀=stock price, K=strike price, r=risk-free rate, T=time to expiration, N=cumulative normal distribution', 'Currency', 'European call option theoretical price', 'Options trading', 'Constant volatility', 'No dividends'),
            ('Capital Asset Pricing Model', 'Portfolio Theory', 'E(R) = Rf + β(E(Rm) - Rf)', 'E(R)=expected return, Rf=risk-free rate, β=beta, E(Rm)=market return', '%', 'Expected return based on systematic risk', 'Asset pricing', 'Efficient markets', 'Beta stability'),
            ('Sharpe Ratio', 'Risk Management', 'SR = (Rp - Rf) / σp', 'Rp=portfolio return, Rf=risk-free rate, σp=portfolio standard deviation', 'Ratio', 'Risk-adjusted return measure', 'Performance evaluation', 'Normal returns', 'Historical data reliability'),
            ('Economic Order Quantity', 'Operations', 'EOQ = √(2DS/H)', 'D=annual demand, S=ordering cost, H=holding cost', 'Units', 'Optimal order quantity minimizing costs', 'Inventory management', 'Constant demand', 'No stockouts'),
            ('Debt-to-Equity Ratio', 'Financial Analysis', 'D/E = Total Debt / Total Equity', 'Total Debt=liabilities, Total Equity=shareholders equity', 'Ratio', 'Financial leverage measure', 'Credit analysis', 'Book values', 'Market value differences'),
            ('Return on Investment', 'Performance', 'ROI = (Gain - Cost) / Cost × 100', 'Gain=investment gain, Cost=investment cost', '%', 'Efficiency of investment', 'Business analysis', 'Accurate cost allocation', 'Time period effects')
        ]
    
    def _get_geological_environmental_data(self) -> List[Tuple]:
        """Get geological and environmental calculations."""
        return [
            # name, category, formula, variables, units, description, applications, environmental_factors, measurement_methods
            ('Darcy\'s Law', 'Hydrogeology', 'Q = -KA(dh/dl)', 'Q=discharge, K=hydraulic conductivity, A=cross-sectional area, dh/dl=hydraulic gradient', 'm³/s', 'Groundwater flow rate', 'Aquifer analysis', 'Temperature, fluid properties', 'Pump tests, piezometers'),
            ('Richter Scale', 'Seismology', 'M = log₁₀(A/A₀)', 'M=magnitude, A=amplitude, A₀=reference amplitude', 'Magnitude units', 'Earthquake magnitude measurement', 'Seismic hazard assessment', 'Distance from epicenter', 'Seismograph recordings'),
            ('Mohs Hardness Scale', 'Mineralogy', 'H = relative hardness (1-10)', 'H=hardness value', 'Mohs units', 'Mineral hardness classification', 'Mineral identification', 'Crystal structure', 'Scratch test'),
            ('Soil Bearing Capacity', 'Geotechnical', 'qult = cNc + γDfNq + 0.5γBNγ', 'c=cohesion, γ=unit weight, Df=depth, B=width, N=bearing capacity factors', 'Pa', 'Ultimate soil bearing capacity', 'Foundation design', 'Soil type, water table', 'Standard penetration test'),
            ('Air Quality Index', 'Environmental', 'AQI = (Ihigh - Ilow)/(BPhigh - BPlow) × (Cp - BPlow) + Ilow', 'I=index values, BP=breakpoints, Cp=pollutant concentration', 'AQI units', 'Air pollution level indicator', 'Public health protection', 'Meteorological conditions', 'Continuous monitoring'),
            ('Carbon Footprint', 'Environmental', 'CF = Σ(Activity × Emission Factor)', 'Activity=consumption/production, Emission Factor=CO₂ equivalent per unit', 'kg CO₂ eq', 'Greenhouse gas emissions calculation', 'Climate change mitigation', 'Energy sources, transportation', 'Life cycle assessment'),
            ('Biodiversity Index', 'Ecology', 'H\' = -Σ(pi × ln(pi))', 'pi=proportion of species i', 'Shannon units', 'Species diversity measure', 'Ecosystem health assessment', 'Sampling methods, habitat', 'Species counting, identification'),
            ('Erosion Rate', 'Geomorphology', 'E = K × R × LS × C × P', 'K=soil erodibility, R=rainfall factor, LS=slope factor, C=cover factor, P=practice factor', 'tons/hectare/year', 'Soil loss prediction', 'Land management', 'Climate, vegetation, topography', 'Sediment traps, surveys'),
            ('Groundwater Recharge', 'Hydrology', 'R = P - ET - RO - ΔS', 'R=recharge, P=precipitation, ET=evapotranspiration, RO=runoff, ΔS=storage change', 'mm/year', 'Aquifer replenishment rate', 'Water resource management', 'Climate, land use, geology', 'Water balance studies'),
            ('Pollution Load', 'Environmental', 'L = C × Q × t', 'L=load, C=concentration, Q=flow rate, t=time', 'kg', 'Contaminant mass transport', 'Water quality management', 'Flow variability, mixing', 'Sampling, flow measurement')
        ]
    
    def calculate(self, equation_name: str, variables: Dict[str, float], category: str = None) -> Dict[str, Any]:
        """Calculate result using specified equation with given variables."""
        try:
            equation = self._find_equation(equation_name, category)
            if not equation:
                return {'error': f'Equation "{equation_name}" not found'}
            
            result = self._evaluate_formula(equation['formula'], variables)
            
            return {
                'equation': equation_name,
                'formula': equation['formula'],
                'variables': variables,
                'result': result,
                'units': equation.get('units', 'Unknown'),
                'description': equation.get('description', '')
            }
            
        except Exception as e:
            self.logger.error(f"Calculation error: {e}")
            return {'error': str(e)}
    
    def _find_equation(self, name: str, category: str = None) -> Optional[Dict]:
        """Find equation in database by name and optional category."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                tables = ['physics_equations', 'math_formulas', 'engineering_calcs', 
                         'chemistry_equations', 'cs_algorithms', 'constants_conversions',
                         'biological_medical', 'financial_economic', 'geological_environmental']
                
                for table in tables:
                    cursor.execute(f'SELECT * FROM {table} WHERE name = ?', (name,))
                    result = cursor.fetchone()
                    
                    if result:
                        columns = [desc[0] for desc in cursor.description]
                        return dict(zip(columns, result))
                
                return None
                
        except Exception as e:
            self.logger.error(f"Equation search error: {e}")
            return None
    
    def _evaluate_formula(self, formula: str, variables: Dict[str, float]) -> float:
        """Safely evaluate mathematical formula with given variables."""
        try:
            safe_dict = {
                '__builtins__': {},
                'abs': abs, 'min': min, 'max': max,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
                'pi': math.pi, 'e': math.e
            }
            
            safe_dict.update(variables)
            formula = self._convert_formula_notation(formula)
            result = eval(formula, safe_dict)
            return float(result)
            
        except Exception as e:
            raise ValueError(f"Formula evaluation failed: {e}")
    
    def _convert_formula_notation(self, formula: str) -> str:
        """Convert mathematical notation to Python-evaluable format."""
        conversions = {
            '×': '*', '÷': '/', '²': '**2', '³': '**3', '√': 'sqrt'
        }
        
        for old, new in conversions.items():
            formula = formula.replace(old, new)
        
        return formula
    
    def search_equations(self, query: str, category: str = None) -> List[Dict]:
        """Search for equations matching query."""
        try:
            results = []
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                tables = ['physics_equations', 'math_formulas', 'engineering_calcs',
                         'chemistry_equations', 'cs_algorithms', 'constants_conversions',
                         'biological_medical', 'financial_economic', 'geological_environmental']
                
                for table in tables:
                    cursor.execute(f'''
                        SELECT * FROM {table} 
                        WHERE name LIKE ? OR description LIKE ? OR formula LIKE ?
                    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                    
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    
                    for row in rows:
                        equation = dict(zip(columns, row))
                        equation['table'] = table
                        results.append(equation)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Equation search error: {e}")
            return []
    
    def convert_units(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Convert between different units."""
        try:
            conversions = {
                ('m', 'ft'): 3.28084, ('ft', 'm'): 0.3048,
                ('kg', 'lb'): 2.20462, ('lb', 'kg'): 0.453592,
                ('Pa', 'psi'): 0.000145038, ('psi', 'Pa'): 6894.76,
                ('J', 'BTU'): 0.000947817, ('BTU', 'J'): 1055.06
            }
            
            conversion_key = (from_unit, to_unit)
            
            if conversion_key in conversions:
                factor = conversions[conversion_key]
                result = value * factor
                
                return {
                    'original_value': value,
                    'original_unit': from_unit,
                    'converted_value': result,
                    'converted_unit': to_unit,
                    'conversion_factor': factor
                }
            else:
                return {'error': f'Conversion from {from_unit} to {to_unit} not supported'}
                
        except Exception as e:
            self.logger.error(f"Unit conversion error: {e}")
            return {'error': str(e)}
    
    def get_equation_stats(self) -> Dict[str, int]:
        """Get statistics about equations in database."""
        try:
            stats = {}
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                tables = [
                    'physics_equations', 'math_formulas', 'engineering_calcs',
                    'chemistry_equations', 'cs_algorithms', 'constants_conversions',
                    'biological_medical', 'financial_economic', 'geological_environmental'
                ]
                
                for table in tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[table] = cursor.fetchone()[0]
                    
            return stats
        except Exception as e:
            self.logger.error(f"Error getting equation stats: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the equation engine."""
        self.logger.info("Universal Equation Engine shutting down")
