using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public enum AdressType
    {
        Home,
        Work,
        Other
    }
    public class AdressEntity : EntityBase
    {
        // Ulice
        [Required, MaxLength(100)]
        public string Street { get; set; } = null!;

        // Cislo popisne
        [Required, MaxLength(20)]
        public string HouseNumber { get; set; } = null!;

        // Cislo orientacni
        [MaxLength(20)]
        public string? OrientationNumber { get; set; }

        // Mesto
        [Required, MaxLength(100)]
        public string City { get; set; } = null!;

        // Kraj
        [MaxLength(100)]
        public string? Region { get; set; }

        // PSC
        [Required, MaxLength(20)]
        public string ZipCode { get; set; } = null!;

        // Stat
        [Required, MaxLength(100)]
        public string Country { get; set; } = null!;

        // Typ adresy
        [Required]
        public AdressType Type { get; set; }
    }
}
