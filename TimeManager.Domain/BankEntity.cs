using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class BankEntity : EntityBase
    {
        // Nazev banky
        [Required, MaxLength(100)]
        public string Name { get; set; } = null!;


        // Kod banky
        [Required, MaxLength(4)]
        public string Code { get; set; } = null!;


        // BIC/SWIFT kod
        [MaxLength(11)]
        public string? BicSwift { get; set; }
    }
}
