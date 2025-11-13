using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class EmployeeEntity : PersonBaseEntity
    {
        // Uzivatelske jmeno
        [MaxLength(100)]
        public string? UserName { get; set; }


        // Spolecnost
        public CompanyEntity? Company { get; set; }


        // Adresy
        public List<AdressEntity> Addresses { get; set; } = new();


        // Kontakty
        public List<ContactEntity> Contacts { get; set; } = new();
    }
}
